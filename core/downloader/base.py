from typing import Callable
from tornado.httpclient import HTTPRequest
from core.scheduler.base import BaseScheduler


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    def __init__(self, scheduler: BaseScheduler = None):
        self.scheduler = scheduler

    def fetch(self, request: HTTPRequest, callback: Callable) -> bool:
        """
        fetch page, and call callback
        :param request: HTTPRequest object
        :param callback: func with HTTPResponse object as arguments
        :return: boolean, start fetch current page or not.
        """
        pass
