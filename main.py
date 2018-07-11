from tornado.ioloop import IOLoop
from core.basespider import BaseSpider

try:
    BaseSpider()
    IOLoop.current().start()
except KeyboardInterrupt:
    IOLoop.current().stop()
