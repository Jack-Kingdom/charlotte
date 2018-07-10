from tornado.ioloop import IOLoop
from core.spider import Spider

try:
    Spider()
    IOLoop.current().start()
except KeyboardInterrupt:
    IOLoop.current().stop()
