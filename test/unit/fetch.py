import asyncio
from charlotte.core.http import HTTPRequest, HTTPResponse
from charlotte.core.fetch import fetch_request
from charlotte.core.loop import default_loop

request = HTTPRequest(protocol='https', host='blog.qiaohong.org', uri='/')


async def handle():
    response = await fetch_request(request)
    print(response)


feature = asyncio.wait([handle(), handle()])
default_loop.run_until_complete(feature)
