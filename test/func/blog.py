import json
from tornado.httpclient import HTTPRequest, HTTPResponse
from charlotte.spider import BaseSpider


class BlogSpider(BaseSpider):

    def start(self):
        yield "https://blog.qiaohong.org/api/v1/articles"

    def parse(self, response):
        lst = json.loads(response.body)

        for item in lst:
            detail_uri = "https://blog.qiaohong.org/api/v1/articles" + "/" + item['slug']
            self.fetch(detail_uri, parser=self.parse_detail)

    def parse_detail(self, response: HTTPResponse):
        detail = json.loads(response.body)
        print(detail)


if __name__ == '__main__':
    BlogSpider().run()
