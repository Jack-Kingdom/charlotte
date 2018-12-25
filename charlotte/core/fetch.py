import asyncio
from charlotte.core.loop import default_loop
from charlotte.core.http import HTTPRequest, HTTPResponse
from charlotte.core.helper import parse_binary_response


async def fetch(address, port=80, message='', timeout=5, ssl=False, domain=None, loop=default_loop):
    future = asyncio.open_connection(host=address, port=port, ssl=ssl,
                                     server_hostname=domain, loop=loop)

    reader, writer = await asyncio.wait_for(future, timeout=timeout, loop=loop)

    writer.write(message)
    return await reader.read()


async def fetch_http(address, message, timeout, loop=default_loop):
    return await fetch(address=address, port=80, message=message, timeout=timeout, ssl=False, domain=None, loop=loop)


async def fetch_https(address, domain, message, timeout, loop=default_loop):
    return await fetch(address=address, port=443, message=message, timeout=timeout, ssl=True, domain=domain, loop=loop)


async def fetch_request(request: HTTPRequest, loop=default_loop) -> HTTPResponse:
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
