import sys
import logging
from charlotte.spider import BaseSpider

logger = logging.getLogger()
logger.setLevel('DEBUG')
logger.addHandler(logging.StreamHandler(sys.stdout))


class MySpider(BaseSpider):
    counter = 0

    def start(self):
        for _ in range(100):
            yield "https://blog.qiaohong.org"

    def parse(self, response):
        self.counter += 1
        print(self.counter, response.code, response.error)


if __name__ == '__main__':
    MySpider().run()
