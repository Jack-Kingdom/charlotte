from charlotte.core.dns import get_cached_dns


class HTTPRequest(object):
    def __init__(self, protocol='http', method='GET', uri='/', host='', version='HTTP/1.1', connection='close',
                 headers=None, body=None, files=None, timeout=5):
        self.protocol = protocol
        self.method = method
        self.uri = uri
        self.host = host
        self.version = version
        self.connection = connection
        self.headers = headers
        self.body = body  # current not used
        self.files = files  # current not used
        self.timeout = timeout
        self._server_ip = None

    def to_bytes(self) -> bytes:
        """
        generate http request bytes
        :return: bytes
        """

        # example 'GET / HTTP/1.1\r\nHost: blg.qiaohong.org\r\nConnection: close\r\n\r\n'
        return '{method} {uri} {version}\r\nHost: {host}\r\nConnection: {connection}\r\n\r\n'. \
            format(method=self.method, uri=self.uri, version=self.version,
                   host=self.host, connection=self.connection).encode()

    @property
    def server_ip(self) -> str:
        """
        return server ip address
        rewrite this value if your want use proxy
        :return:
        """
        if not self._server_ip:
            self._server_ip = get_cached_dns(self.host)
        return self._server_ip

    def set_server_ip(self, address: str) -> None:
        self._server_ip = address


class HTTPResponse(object):

    def __init__(self, request: HTTPRequest, version=None, status_code=None, reason=None, headers=None, body=None):
        self.request = request
        self.version = version
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.body = body
