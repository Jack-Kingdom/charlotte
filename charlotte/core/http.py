class HTTPRequest(object):
    def __init__(self, protocol='http', method='GET', uri='/', host='', version='HTTP/1.0', connection='close',
                 headers=None, body=None, files=None):
        self.protocol = protocol
        self.method = method
        self.uri = uri
        self.host = host
        self.version = version
        self.connection = connection
        self.headers = headers
        self.body = body
        self.files = files


class HTTPResponse(object):

    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body
