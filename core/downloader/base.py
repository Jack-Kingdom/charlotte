from typing import Callable
from tornado.httpclient import HTTPRequest, HTTPResponse
from core.scheduler.base import BaseScheduler
from core import setting


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
