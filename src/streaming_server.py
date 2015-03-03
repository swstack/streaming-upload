import json
import hashlib

import os

from paste import httpserver
from webapp2 import WSGIApplication, Route, RequestHandler
from database import Database


db = Database('localhost')


class StreamingFileHandler(RequestHandler):
    file_store = '/tmp'

    @classmethod
    def from_deps(cls, db, *args, **kwargs):
        return cls(db, *args, **kwargs)

    def get(self, file_id):
        """Get meta data for file(s)

        If the file_id param
        """

        self.response.write('Hello, webapp2!')

    def put(self, file_id=None):
        """Read the contents of the body and write to disk

        If no file_id is provided we will create a new file.  This method will
        return an ID so that the client can look up the file at at later time.
        """

        if file_id is None or file_id == '':
            file_id = str(db.get_unique_file_id())
        else:
            file_id = file_id.strip('/')

        # Open a file on disk located under `self.file_store`
        file_path = os.path.join(self.file_store, file_id)
        with open(file_path, 'wb') as out:

            md5_checksum = hashlib.md5()

            # Start reading the file in 128 byte chunks
            while True:
                chunk = self.request.body_file.read(128)
                if chunk == '':
                    break

                # Write the chunk out to disk and update our checksum
                out.write(chunk)
                md5_checksum.update(chunk)

        db.update_file(file_id,
                       file_path,
                       os.path.getsize(file_path),
                       md5_checksum.digest())

        self.response.write(json.dumps({'file_id': file_id}))


def main():
    """Start the streaming file-upload server"""

    app = WSGIApplication(

        # Routes
        [
            Route('/file/<file_id:(.*)>',
                  handler=StreamingFileHandler,
                  methods=['PUT', 'GET'])
        ],

        # Other options
        debug=True
    )

    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()
