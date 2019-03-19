import asyncio
from charlotte.core.fetch import fetch_request
from charlotte.core.loop import default_loop
from charlotte.core.helper import url2request


async def handle():
    try:
        request = url2request('https://www.wandoujia.com/apps/com.youzu.bong.aligames')
        response = await fetch_request(request)
    except Exception as e:
        print("err:", e)
    else:
        print(response.status_code, response.headers, response.body)


feature = asyncio.wait([handle() for _ in range(100)])

try:
    default_loop.run_until_complete(feature)
finally:
    default_loop.close()
