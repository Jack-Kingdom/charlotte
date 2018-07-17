from tornado.httpclient import HTTPRequest, HTTPResponse
from charlotte.spider import BaseSpider
from charlotte.scheduler import QueueScheduler
from charlotte.downloader import AsyncDownloader


class MySpider(BaseSpider):
    downloader = AsyncDownloader()
    scheduler = QueueScheduler(downloader)

    counter = 0

    def start(self):
        for _ in range(5):
            yield HTTPRequest("https://blog.qiaohong.org")

    def parse(self, response: HTTPResponse):
        self.counter += 1
        print(self.counter, response.code, response.error)


if __name__ == '__main__':
    MySpider().run()
