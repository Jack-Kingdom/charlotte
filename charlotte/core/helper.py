"""
some helper method in this file
"""

from charlotte.core.http import HTTPResponse


def parse_binary_response(binary: bytes, response: HTTPResponse) -> HTTPResponse:
    """
    parse a binary http response to HTTPResponse object
    """
    meta, other = binary.split(b'\r\n', 1)

    # parse meta info
    version, status_code, reason = meta.split(b' ', 2)
    response.version, response.status_code, response.reason = version.decode(), int(status_code), reason.decode()

    raw_headers, raw_body = other.split(b'\r\n\r\n')

    # parse header
    headers = {}
    str_headers = raw_headers.decode('utf-8')  # decode header first
    for str_header in str_headers.split('\r\n'):
        key, value = str_header.split(': ')
        headers.setdefault(key, value)

    response.headers, response.body = headers, raw_body
    return response
