import time

from pymongo import MongoClient
from bson.binary import MD5_SUBTYPE, Binary


class Database(object):
    """Encapsulation of the MongoDB database and collection(s)

    For the context of this application this class will only provide an API
    for storing and fetching files.
    """

    def __init__(self, host, port=27017):
        self._client = MongoClient(host, port)

    @property
    def _files(self):
        files_collection = self._client.files_collection
        return files_collection.files

    def get_file_data(self, file_id=None):
        """Return file data for one or more files based on file_id

        This method will always return an iterable
        """

        if file_id:
            return self._files.find({'_id': file_id})
        else:
            return self._files.find({})

    def update_file(self, file_id, path, size, checksum):
        """Record a file in the database with it's meta-data"""

        # TODO: Could store checksum as hexlified plain text

        meta_data = {
            'timestamp': int(time.time()),              # UNIX Timestamp (secs since epoch)
            'path': path,                               # Path to file
            'size': int(size),                          # File size in bytes
            'checksum': Binary(checksum, MD5_SUBTYPE),  # MD5 Checksum
        }

        if self._files.find_one(file_id) is None:
            # Document doesn't exist yet
            self._files.insert({'_id': file_id})

        self._files.update({'_id': file_id}, {'$set': meta_data})

    def get_unique_file_id(self):
        """Create a blank document in the files database and return it's ID"""

        return self._files.insert({})
