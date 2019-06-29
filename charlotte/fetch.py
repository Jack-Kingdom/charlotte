import asyncio
from charlotte.http import HTTPRequest, HTTPResponse
from charlotte.helper import parse_binary_response


async def fetch(address, port=80, message='', timeout=5, ssl=False, domain=None, loop=None):
    future = asyncio.open_connection(host=address, port=port, ssl=ssl,
                                     server_hostname=domain, loop=loop)

    reader, writer = await asyncio.wait_for(future, timeout=timeout, loop=loop)

    writer.write(message)
    return await reader.read()


def fetch_http(address, message, timeout, loop=None):
    return fetch(address=address, port=80, message=message, timeout=timeout, ssl=False, domain=None, loop=loop)


def fetch_https(address, domain, message, timeout, loop=None):
    return fetch(address=address, port=443, message=message, timeout=timeout, ssl=True, domain=domain, loop=loop)


async def fetch_request(request: HTTPRequest, loop=None) -> HTTPResponse:
    """
    wrapper for fetch & fetch_* method,
    handle HTTPRequest object to HTTPResponse
    """

    binary = None

    if request.protocol == 'http':
        binary = await fetch_http(request.server_ip, request.to_bytes(), request.timeout, loop)

    if request.protocol == 'https':
        binary = await fetch_https(request.server_ip, request.host, request.to_bytes(), request.timeout, loop)

    if binary:
        response = HTTPResponse(request=request)
        return parse_binary_response(binary, response)

    raise NotImplementedError("{0} protocol not implement".format(request.protocol))
