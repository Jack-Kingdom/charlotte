import asyncio
from charlotte.core.http import HTTPRequest, HTTPResponse
from charlotte.core.fetch import fetch_request
from charlotte.core.loop import default_loop
from charlotte.core.helper import url2request
from charlotte.scheduler.base import BaseScheduler
from charlotte.spider.base import BaseSpider


# async def handle():
#     try:
#         request = url2request('https://blog.qiaohong.org/api/v1/articles')
#         response = await fetch_request(request)
#     except Exception as e:
#         print("err:", e)
#     else:
#         print(response.status_code, response.headers, response.body)
#
#
# feature = asyncio.wait([handle() for _ in range(100)])
#
# try:
#     default_loop.run_until_complete(feature)
# finally:
#     default_loop.close()

class Spider(BaseSpider):

    async def on_start(self):
        response = await self.fetch(url2request('https://blog.qiaohong.org/api/v1/articles'), parser=self.parse)
        # print(response)

    def parse(self, res: HTTPResponse):
        print(res.body)


if __name__ == '__main__':
    Spider().run()
