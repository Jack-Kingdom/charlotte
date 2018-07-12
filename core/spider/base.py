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
                 scheduler: BaseScheduler = None,
                 downloader: BaseDownloader = None):
        self.scheduler = scheduler
        self.downloader = downloader

    def start(self) -> Generator:
        """
        Spider start function. Call once on spider start.
        :return: a generator of HTTPRequest object
        """
        pass

    def parse(self, response: HTTPResponse) -> Generator:
        """
        Default parse function.
        :param response:
        :return:
        """
        pass
