from paste import httpserver
from webapp2 import WSGIApplication, Route, RequestHandler
from database import Database
from functools import wraps
import json
import os


db = Database('localhost')


def _request_handler_factory(handler, database):
    """Factory for making request handlers

    The reasoning behind this factory is because globals are bad, and this way
    we can inject the custom `db` dependency into he request handlers.
    """

    def closure(*args, **kwargs):
        return handler.from_deps(database, *args, **kwargs)

    closure.__doc__ = 'foo'
    closure.__module__ = 'bar'
    return closure


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

    def put(self):
        """Read the contents of the body and write to disk

        This method will return an ID so that the client can look up the file at
        at later time
        """

        new_file_id = db.get_unique_file_id()
        with open(os.path.join(self.file_store, new_file_id), 'wb'):
            pass

        x = 5


_routes = [

    Route('/file/(\d+)',
          handler=StreamingFileHandler,
          methods=['GET']),

    Route('/file/',
          handler=StreamingFileHandler,
          methods=['PUT'])
]

app = WSGIApplication(_routes, debug=True)


def main():
    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()
