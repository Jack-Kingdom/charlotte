import asyncio
from charlotte.core.loop import default_loop
from charlotte.core.http import HTTPRequest, HTTPResponse


async def fetch(host, port=80, message='', timeout=5, ssl=False, hostname=None, loop=default_loop):
    future = asyncio.open_connection(host=host, port=port, ssl=ssl,
                                     server_hostname=hostname, loop=loop)

    reader, writer = await asyncio.wait_for(future, timeout=timeout, loop=loop)

    writer.write(message.encode())
    return await reader.read()


async def fetch_http(host, message, timeout, loop=default_loop):
    return await fetch(host=host, port=80, message=message, timeout=timeout, ssl=False, hostname=None, loop=loop)


async def fetch_https(host, hostname, message, timeout, loop=default_loop):
    return await fetch(host=host, port=443, message=message, timeout=timeout, ssl=True, hostname=hostname, loop=loop)


async def fetch_request(request: HTTPRequest, loop=default_loop) -> HTTPResponse:
    pass
