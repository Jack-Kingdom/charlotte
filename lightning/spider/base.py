from typing import Generator
from tornado.ioloop import IOLoop
from ..scheduler.base import BaseScheduler
from tornado.httpclient import HTTPRequest, HTTPResponse
from .. import setting


class BaseSpider(object):
    """
    Interface for spider.
    """

    def __init__(self,
                 scheduler: BaseScheduler = None):
        self.scheduler = scheduler

    def start(self) -> Generator:
        """
        Spider start function. Call once on spider start.
        :return: a generator of tuple, HTTPRequest object and callback func
        """
        pass

    def parse(self, response: HTTPResponse) -> Generator:
        """
        Default parse function.
        todo: how to handle this function's request objects
        :param response:
        :return:
        """
        pass

    def run(self):
        """
        run spider
        :return: None
        """

        for item in self.start():
            if isinstance(item, HTTPRequest):
                req, cb = item, self.parse
            elif isinstance(item, tuple):
                assert isinstance(item[0], HTTPRequest) and isinstance(item[1], function)
                req, cb = item
            else:
                raise TypeError('start func return type error')
            self.scheduler.put(req, cb)

        loop = IOLoop.instance()
        try:
            loop.start()
        except KeyboardInterrupt:
            loop.stop()
