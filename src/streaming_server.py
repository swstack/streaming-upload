import json
import hashlib
import operator
import base64

import os

from paste import httpserver
from webapp2 import WSGIApplication, Route, RequestHandler
from database import Database


db = Database('localhost')


class StreamingFileHandler(RequestHandler):
    """Request handler for route /file/<id>"""

    file_store = '/tmp'

    def get(self, file_id=None):
        """Get meta data for file(s)

        TODO: Consider streaming response
        """

        if file_id is None or file_id == '':
            file_id = None
        else:
            file_id = file_id.strip('/')

        documents = []
        for document in db.get_file_data(file_id=file_id):
            documents.append(document)

        documents.sort(key=operator.itemgetter('size'))  # Sort in place
        self.response.write(json.dumps(documents))

    def put(self, file_id=None):
        """Read the contents of the body and write to disk

        If no file_id is provided we will create a new file.  This method will
        return an ID so that the client can look up the file at at later time.

        NOTE: The PUT method in a pure REST implementation would likely not allow
        the creation of files, only updating existing ones.  We could introduce a
        POST method to the root collection /file/ to create a file and return the
        newly created file ID.
        
        This implementation of PUT also allows user to specify any arbitrary file_id
        and it will create or update that file, which may not be a good idea or secure.
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

        try:
            file_size = os.path.getsize(file_path)
        except OSError:
            # File path likely doesn't exist ...not a good situation
            file_size = 0

        db.update_file(file_id,
                       file_path,
                       file_size,
                       md5_checksum.hexdigest())

        self.response.write(json.dumps({'file_id': file_id}))


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


def main():
    """Start the streaming file-upload server"""

    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()
