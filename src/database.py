import datetime

from pymongo import MongoClient, ASCENDING


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

        This method will always return an iterable and will be sorted based
        file size in ascending order
        """

        if file_id:
            unsorted = self._files.find({'_id': file_id})
        else:
            unsorted = self._files.find({})

        return unsorted.sort('size', ASCENDING)

    def update_file(self, file_id, path, size, checksum):
        """Record a file in the database with it's meta-data"""

        # TODO: Could store checksum as hexlified plain text

        meta_data = {
            'timestamp': datetime.datetime.now(),
            'path': path,
            'size': int(size),
            'checksum': checksum,
        }

        if self._files.find_one(file_id) is None:
            # Document doesn't exist yet
            self._files.insert({'_id': file_id})

        self._files.update({'_id': file_id}, {'$set': meta_data})

    def get_unique_file_id(self):
        """Create a blank document in the files database and return it's ID"""

        return self._files.insert({})
