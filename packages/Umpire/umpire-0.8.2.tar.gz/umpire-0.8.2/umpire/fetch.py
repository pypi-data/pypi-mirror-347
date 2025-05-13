"""fetch.py"""

import sys, os, urllib, time, traceback
from . import cache, config
from multiprocessing import Value
from maestro.core import module
from maestro.aws import s3
from maestro.tools import file as mfile
import logging
logger = logging.getLogger(__name__)

CACHE_LOCATION_KEYS = ["c", "cache-location"]
DEPENDENCY_NAME_KEYS = ["n", "name"]
DEPENDENCY_PLATFORM_KEYS = ["p", "platform"]
DEPENDENCY_REPOSITORY_KEYS = ["r", "repository"]
DEPENDENCY_VERSION_KEYS = ["v", "version"]
HELP_KEYS = ["h", "help"]

class EntryState(object):
    CACHE = 0
    DOWNLOADED = 1
    UPDATED = 2

class EntryError(Exception):
    pass

class FetchModule(module.AsyncModule):

    # Required ID of this module
    id = "fetch"

    #Initialize shm value #TODO: Near future
    progress = Value('d', 0.0)

    # Version of dependency (Default latest) #TODO: Future
    dependency_version = None

    ### Required Variables for this Module ###
    #Location of the cache root folder (r+w by every user)
    cache_root = None

    #Name of dependency to fetch
    dependency_name = None

    #Name of platform of dependency to fetch
    dependency_platform = None

    #The repository to fetch the dependency, or to verify the integrity from
    dependency_repo = None

    #Is the dependency going to be linked?
    dependency_is_link = None

    #Is the dependency going to be extracted after the download
    dependency_unpack = None

    #Are we going to check if this dependency has changed in the remote?
    keep_updated = None

    log_level=None

    def run(self,kwargs):
        logger = logging
        FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
        logger.basicConfig(format=FORMAT, stream=sys.stdout, level=self.log_level)
        logger.debug("Running Fetch")
        #Verify argument validity
        self.__verify_arguments__()

        #Get cache name from remote url
        cache_name = self.get_cache_name()

        #Get cache path
        cache_path = os.path.join(self.cache_root, cache_name)

        logger.debug(f"Cache path: {cache_path}")

        #Get cache object (will raise an exception if it doesn't exist)
        cache_obj = cache.LocalCache(cache_path, host_id=config.default_host_id, log_level=self.log_level)

        full_url = s3.join_s3_url(self.dependency_repo, self.dependency_platform, self.dependency_name, self.dependency_version)

        cache_obj.lock(os.path.join(cache_path,self.dependency_platform, self.dependency_name, self.dependency_version))
        #Try to get entry from cache
        entry = cache_obj.get(self.dependency_platform, self.dependency_name, self.dependency_version)

        #Set state
        if entry is None:
            state = EntryState.DOWNLOADED
        else:
            state = EntryState.CACHE

        #Verify Remote sha256 if updating
        if self.keep_updated and state == EntryState.CACHE:
            bucket,prefix = s3.parse_s3_url(full_url)
            checksums = list()
            try:
                for file in s3.find_files(bucket, prefix, anonymous=False, sha256=True ):
                    checksums.append(file[1])
            except:
                logger.debug(f"{traceback.print_exc()}")
                for file in s3.find_files(bucket, prefix, anonymous=True, sha256=True ):
                    checksums.append(file[1])

            if entry.md5 not in checksums:
                state = EntryState.UPDATED

        #We need to download the file, it wasn't in the cache
        if state == EntryState.DOWNLOADED or state == EntryState.UPDATED:

            if state == EntryState.DOWNLOADED:
                logger.info(self.format_entry_name() + ": Not in cache")
            else:
                logger.info(self.format_entry_name() + ": Cache is obsolete")

            logger.info(self.format_entry_name() + ": Downloading " + full_url)

            #Get Downloader
            downloader = s3.AsyncS3Downloader(None)

            #Set Downloader arguments
            downloader.source_url = full_url+"/"
            downloader.sha256 = True
            downloader.destination_path = os.path.join(self.cache_root, "downloading") + os.sep
            downloader.start()

            #Wait for downloader to finish #TODO: Do something with the reported progress
            while downloader.status != 2:
                time.sleep(0.5)

            #Check for an exception, if so bubble it up
            if downloader.exception is not None:
                logger.error(f"Exception!!! {downloader.exception}")
                # raise downloader.exception
                sys.exit(1)
            logger.info(self.format_entry_name() + ": Download complete")
            logger.debug(f"Result: {downloader.result}")
            if downloader.result is None or len(downloader.result) == 0:
                raise EntryError(self.format_entry_name() + ": Unable to find remote entry '" + full_url + "'")

            #Iterate of the result (downloaded files)
            for item, checksum in downloader.result:
                local_file_checksum = mfile.sha256_checksum(item, checksum)
                logging.debug(f"sha 256 checksum local_file: {local_file_checksum} remote: {checksum}")
                if checksum != local_file_checksum:
                    logger.warning(self.format_entry_name() + ": WARNING: Downloaded file does not match the checksum on the server")
                    logger.warning(self.format_entry_name() + ": WARNING: local:\t" + str(local_file_checksum))
                    logger.warning(self.format_entry_name() + ": WARNING: server:\t" + str(checksum))
                if self.dependency_unpack:
                    print(self.format_entry_name() + ": Unpacking...")
                    logger.info (self.format_entry_name() + ": Unpacking...")
                #Put will unlock
                cache_obj.put(item,self.dependency_platform, self.dependency_name, self.dependency_version, unpack_bol=self.dependency_unpack, checksum=checksum)
            entry = cache_obj.get(self.dependency_platform, self.dependency_name, self.dependency_version)
            if entry is None:
                raise EntryError(self.format_entry_name() + ": Error retrieving entry from cache.")
        cache_obj.unlock(os.path.join(cache_path,self.dependency_platform, self.dependency_name, self.dependency_version))
        #Entry is not None, return all the files listed in the entry that aren't the configuration files
        return [os.path.abspath(os.path.join(entry.path,f)) for f in os.listdir(entry.path) if f != ".umpire"], state


    def format_entry_name(self):
        return str(self.dependency_platform) + "/" + str(self.dependency_name) + " " + str(self.dependency_version)

    def __verify_arguments__(self):
        if not self.dependency_repo:
            raise ValueError("You must specify a valid repository URL.")
        if not self.dependency_name:
            raise ValueError("You must specify a valid name for the dependency.")
        if not self.dependency_platform:
            raise ValueError("You must specify a valid platform for the dependency.")
        if not self.dependency_version:
            raise ValueError("You must specify a valid version for the dependency.")
        if not self.dependency_is_link:
            # Not used
            pass
        if not self.keep_updated:
            self.keep_updated = False
        if not isinstance(self.dependency_unpack,bool):
            logger.info(str(self.dependency_unpack))
            raise ValueError("You must specify whether the dependency should be unpacked or not")

    def get_cache_name(self):
        try:
            bucket, prefix = s3.parse_s3_url(self.dependency_repo)
            return bucket + ".s3"
        except ValueError:
            raise ValueError("Only URLs formatted as: s3://{bucket}/ are currently accepted.")

    def __parse_kwargs__(self,kwargs):
        if kwargs is None:
            return
        for key, val in kwargs.items():
            if key in CACHE_LOCATION_KEYS:
                self.cache_repo = val
            elif key in DEPENDENCY_NAME_KEYS:
                self.dependency_name = val
            elif key in DEPENDENCY_PLATFORM_KEYS:
                self.dependency_platform = val
            elif key in DEPENDENCY_REPOSITORY_KEYS:
                self.dependency_repo = val
            elif key in DEPENDENCY_VERSION_KEYS:
                self.dependency_version = val

