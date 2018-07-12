import functools
from typing import Callable
from tornado.httpclient import HTTPRequest
from core.downloader.base import BaseDownloader
from core.utils.call import call_increase, call_decrease


def cb_decrease(value):
    """
    decrease concurrency when put func's callback called.
    :return: decorator
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(obj: BaseScheduler, request: HTTPRequest, callback: Callable):
            callback = call_decrease(value)(callback)

            return func(obj, request, callback)

        return inner_wrapper

    return wrapper


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def __init__(self, downloader: BaseDownloader,
                 max_concurrency: int = 64):
        self.downloader = downloader
        self.max_concurrency = max_concurrency
        self.concurrency = 0

        # increase concurrency when fetch func called
        self.downloader.fetch = call_increase(self.concurrency)(self.downloader.fetch)

    def get(self) -> HTTPRequest:
        """
        get request item from scheduler
        :return: HTTPRequest Object or None
        """
        pass

    @cb_decrease
    def put(self, request: HTTPRequest, callback: Callable) -> None:
        """
        put request item from scheduler
        :param request:
        :param callback: call back func
        :return: None
        """
        pass

    def empty(self) -> bool:
        """
        scheduler's queue empty or not
        :return: Boolean, True or False
        """
        pass
