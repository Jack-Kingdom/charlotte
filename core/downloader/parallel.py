import functools
from typing import Callable
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from core.scheduler.base import BaseScheduler
from core.downloader.base import BaseDownloader


def call_decrease(value):
    """
    decrease value when func called.
    :param value: integer
    :return: decorator
    """

    value -= 1

    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


class ParallelDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    def __init__(self, scheduler: BaseScheduler,
                 max_concurrency: int = 64):
        super(ParallelDownloader, self).__init__(scheduler)
        self.concurrency = 0
        self.max_concurrency = max_concurrency
        self.client = httpclient.AsyncHTTPClient()

    def fetch(self, request: HTTPRequest, callback: Callable) -> bool:
        """
        fetch request and return response
        """

        if self.concurrency >= self.max_concurrency:
            return False

        self.concurrency += 1
        self.client.fetch(request, call_decrease(self.concurrency)(callback))

        while not self.scheduler.empty() and self.concurrency < self.max_concurrency:
            req = self.scheduler.get()
            if not req:
                self.fetch(req, callback)

        return True
