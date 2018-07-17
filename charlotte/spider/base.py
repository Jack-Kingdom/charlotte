from typing import Generator
from tornado.ioloop import IOLoop
from tornado.httpclient import HTTPRequest, HTTPResponse
from .. import setting


class BaseSpider(object):
    """
    Interface for spider.
    """

    scheduler = None

    def start(self) -> Generator:
        """
        Spider start function. Call once on spider start.
        :return: a generator of tuple, HTTPRequest object and callback func
        """
        pass

    def parse(self, response: HTTPResponse) -> Generator:
        """
        Default parse function.
        :param response:
        :return:
        """
        pass

    def run(self):
        """
        run spider
        :return: None
        """

        for request in self.start():
            assert isinstance(request, HTTPRequest)

            if not getattr(request, 'parser', None):
                setattr(request, 'parser', self.parse)

            self.scheduler.put(request)

        loop = IOLoop.current(instance=True)
        try:
            loop.start()
        except KeyboardInterrupt:
            loop.stop()
