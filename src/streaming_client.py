import requests

HOST = 'localhost'
PORT = 8080

my_not_so_large_file = """
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
sadfjf3098f324j09fj8a9sdh8ff92308fjsl;kdajfj1243890jfasdh9fp8hf120f8h
"""


def _make_uri(file_id):
    if file_id is None:
        location = 'file'
    else:
        location = 'file/%s' % file_id
    return "http://{host}:{port}/{location}/".format(
        host=HOST,
        location=location,
        port=PORT
    )


def get(file_id=None):
    uri = _make_uri(file_id)
    print "Performing GET to %s" % uri
    response = requests.get(uri)
    return response.json()


def put(file_id=None):
    uri = _make_uri(file_id)
    print "Performing PUT to %s" % uri
    response = requests.put(
        uri,
        data=my_not_so_large_file,
        headers={'content-type': 'text/plain'},
    )
    return response


def main():
    # print get()
    # print get('foobar')
    # print put('newidizzle')
    print put()


if __name__ == '__main__':
    main()