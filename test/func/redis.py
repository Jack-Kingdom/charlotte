import sys
import logging
from redis import Redis
from charlotte.spider import BaseSpider
from charlotte.scheduler import RedisScheduler

logger = logging.getLogger()
logger.setLevel('DEBUG')
logger.addHandler(logging.StreamHandler(sys.stdout))

counter = 0


class MySpider(BaseSpider):
    scheduler = RedisScheduler(redis=Redis(host='localhost', port=6379))

    def start(self):
        for _ in range(100):
            yield "https://blog.qiaohong.org"

    def parse(self, response):
        global counter
        counter += 1
        print(counter, response.code, response.error)


if __name__ == '__main__':
    MySpider().run()
