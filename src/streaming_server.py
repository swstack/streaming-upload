from paste import httpserver
from webapp2 import WSGIApplication, Route, RequestHandler
import json


class StreamingFileHandler(RequestHandler):
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
        x = 4


_routes = [
    Route('/file/(\d+)', handler=StreamingFileHandler, methods=['GET']),
    Route('/file/', handler=StreamingFileHandler, methods=['PUT'])
]


def main():
    app = WSGIApplication(_routes, debug=True)
    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()
