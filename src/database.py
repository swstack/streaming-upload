from pymongo import MongoClient
import os
import md5


class Database(object):
    """Encapsulation of the MongoDB database and collection(s)

    For the context of this application this class will only provide an API
    for storing and fetching files.
    """

    FILE_COLLECTION = 'files'

    def __init__(self, host, port=27017):
        self._client = MongoClient(host, port)

    @property
    def _files(self):
        files_collection = self._client.files_collection
        return files_collection.files

    def record_file(self, file_path):
        """Record a file in the database with it's meta-data"""

    def get_unique_file_id(self):
        """Create a blank document in the files database and return it's ID"""

        files_collection = self._client.files
        return self._files.insert({})


if __name__ == "__main__":
    db = Database()
    cli = db.connect('localhost')
    print cli.foobar
