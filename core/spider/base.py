from typing import Generator
from core.scheduler.base import BaseScheduler
from core.downloader.base import BaseDownloader
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
        :param response:
        :return:
        """
        pass

    def run(self):
        """
        Spider run method
        :return:
        """

        for item in self.start():
            assert len(item) == 1 or len(item) == 2
            assert isinstance(item[0], HTTPRequest)
            req, cb = item if len(item) == 2 else item[0], self.parse
            self.scheduler.put(req, cb)
