from typing import Callable
from tornado.httpclient import HTTPRequest
from core.scheduler.base import BaseScheduler


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    def __init__(self, scheduler: BaseScheduler = None):
        self.concurrency = 0

    def fetch(self, request: HTTPRequest, callback: Callable) -> None:
        """
        fetch request and return response
        :param request: HTTPRequest object that need to fetch
        :param callback: func with HTTPResponse object as arguments
        :return: None
        """
        pass
