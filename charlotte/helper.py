"""
some helper method in this file
"""

import hashlib
from urllib.parse import urlparse
from charlotte.http import HTTPRequest, HTTPResponse

CRLF = b'\r\n'


def url2request(url: str) -> HTTPRequest:
    """
    from url parse a basic HTTPRequest object
    :return:
    """

    rst = urlparse(url)
    return HTTPRequest(protocol=rst.scheme, method="GET",
                       uri=rst.path + '?' + rst.query if rst.query else rst.path,
                       host=rst.netloc.split(':')[0])


def parse_binary_response(binary: bytes, response: HTTPResponse) -> HTTPResponse:
    """
    parse a binary http response to HTTPResponse object
    """
    meta, other = binary.split(CRLF, 1)

    # parse meta info
    version, status_code, reason = meta.split(b' ', 2)
    response.version, response.status_code, response.reason = version.decode(), int(status_code), reason.decode()

    raw_headers, raw_body = other.split(CRLF * 2, 1)

    # parse header
    headers = {}
    str_headers = raw_headers.decode('utf-8')  # decode header first
    for str_header in str_headers.split(CRLF.decode()):
        key, value = str_header.split(': ')
        headers.setdefault(key, value)

    # todo handle compressed response

    response.headers = headers
    response.body = parse_chunked_body(raw_body) if headers.get('Transfer-Encoding') == 'chunked' else raw_body

    return response


def parse_chunked_body(raw_body):
    body, left = b'', raw_body

    while left:
        hex_len, left = left.split(CRLF, 1)
        decimal_len = int(hex_len, 16)
        body, left = body + left[:decimal_len], left[decimal_len + len(CRLF):]

    return body


def str2hash(origin: str):
    """
    generate hash for current str
    :param origin: original str
    :return: hash string
    """
    url = origin.encode('utf-8')

    return hashlib.sha256(url).hexdigest()
