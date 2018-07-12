from typing import Callable
from tornado.httpclient import HTTPRequest
from core.scheduler.base import BaseScheduler


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    def fetch(self, request: HTTPRequest, callback: Callable) -> bool:
        """
        Fetch page, and call callback.
        Return True is request start, else return False.
        :param request: HTTPRequest object
        :param callback: func with HTTPResponse object as arguments
        :return: boolean, start fetch current page or not.
        """
        pass
