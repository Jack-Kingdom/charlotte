from tornado.ioloop import IOLoop
from core.spider import BaseSpider

try:
    spider = BaseSpider()
    spider.run()
except KeyboardInterrupt:
    IOLoop.current().stop()
