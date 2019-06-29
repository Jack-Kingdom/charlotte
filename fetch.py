import json
import asyncio
from charlotte.spider import BaseSpider


class Spider(BaseSpider):

    async def on_start(self):
        response = await self.fetch('https://blog.qiaohong.org/api/v1/articles')

        items = json.loads(response.body)

        await asyncio.wait(
            [self.fetch('https://blog.qiaohong.org/api/v1/articles/' + item['slug'],
                        parser=self.parse_detail) for item in items['data']['articles']])

    def parse_detail(self, res):
        print(res.body.decode('utf-8'))


if __name__ == '__main__':
    Spider().run()
