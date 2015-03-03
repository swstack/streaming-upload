import unittest
import streaming_server
import webapp2
import mock


class TestStreamingServer(unittest.TestCase):

    def setUp(self):
        streaming_server.db.get_file_data = mock.Mock(return_value=[])
        streaming_server.db.update_file = mock.Mock()
        streaming_server.db.get_unique_file_id = mock.Mock(return_value=1)

    def test_root_404(self):
        request = webapp2.Request.blank('/')
        response = request.get_response(streaming_server.app)
        self.assertEqual(response.status_int, 404)

    def test_get_file_with_id(self):
        request = webapp2.Request.blank('/file/foobar')
        request.method = 'GET'
        response = request.get_response(streaming_server.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, '[]')

    def test_get_file_no_id(self):
        request = webapp2.Request.blank('/file/')
        request.method = 'GET'
        response = request.get_response(streaming_server.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, '[]')

    def test_put_file_with_id(self):
        m = mock.mock_open()
        request = webapp2.Request.blank('/file/foobar')
        request.method = 'PUT'
        request.body = 'mytestdata'
        with mock.patch('__builtin__.open', m, create=True):
            response = request.get_response(streaming_server.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, '{"file_id": "foobar"}')
        handle = m()
        handle.write.assert_called_once_with('mytestdata')

    def test_put_file_no_id(self):
        m = mock.mock_open()
        request = webapp2.Request.blank('/file/')
        request.method = 'PUT'
        request.body = 'mytestdata'
        with mock.patch('__builtin__.open', m, create=True):
            response = request.get_response(streaming_server.app)
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.body, '{"file_id": "1"}')
        handle = m()
        handle.write.assert_called_once_with('mytestdata')