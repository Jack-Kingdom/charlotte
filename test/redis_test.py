from redis import Redis
from tornado.httpclient import HTTPRequest, HTTPResponse
from charlotte.spider import BaseSpider
from charlotte.scheduler import RedisScheduler

counter = 0


class MySpider(BaseSpider):

    scheduler = RedisScheduler(redis=Redis(host='localhost', port=6379))

    def start(self):
        for _ in range(100):
            yield HTTPRequest("https://blog.qiaohong.org")

    def parse(self, response: HTTPResponse):
        global counter
        counter += 1
        print(counter, response.code, response.error)


if __name__ == '__main__':
    MySpider().run()
