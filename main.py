from tornado.httpclient import HTTPRequest, HTTPResponse
from core.spider import BaseSpider
from core.scheduler import QueueScheduler
from core.downloader import AsyncDownloader


class MySpider(BaseSpider):
    counter = 0

    def start(self):
        for _ in range(1000):
            yield HTTPRequest("https://blog.qiaohong.org")

    def parse(self, response: HTTPResponse):
        self.counter += 1
        print(self.counter, response.code, response.error)


if __name__ == '__main__':
    spider = MySpider(QueueScheduler(AsyncDownloader()))
    spider.run()
