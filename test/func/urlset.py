import sys
import logging
from charlotte.spider import BaseSpider
from charlotte.scheduler import QueueScheduler
from charlotte.middleware import URLSetFilter

logger = logging.getLogger()
logger.setLevel('DEBUG')
logger.addHandler(logging.StreamHandler(sys.stdout))


class MySpider(BaseSpider):
    counter = 0

    scheduler = QueueScheduler(middleware=(URLSetFilter(),))

    def start(self):
        for _ in range(100):
            yield "https://blog.qiaohong.org"

    def parse(self, response):
        self.counter += 1
        print(self.counter, response.code, response.error)


if __name__ == '__main__':
    MySpider().run()
