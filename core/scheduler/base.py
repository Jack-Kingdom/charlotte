import time
from typing import Callable, Tuple
from tornado.httpclient import HTTPRequest
from core.downloader.base import BaseDownloader
from core.utils.call import call_increase, call_decrease
from core import setting


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def __init__(self, downloader: BaseDownloader):
        self.downloader = downloader
        self.max_concurrency = setting.max_concurrency
        self.concurrency = 0

        # increase concurrency when fetch func called
        flag_string = 'cb_decrease_flag'
        if not getattr(self.downloader.fetch, flag_string, False):
            self.downloader.fetch = call_increase(self.concurrency)(self.downloader.fetch)
            setattr(self.downloader.fetch, flag_string, True)

    def get(self) -> Tuple[HTTPRequest, Callable]:
        """
        get request obj and callback func from scheduler
        :return: tuple of HTTPRequest and Callable func or None
        """
        pass

    def put(self, request: HTTPRequest, callback: Callable) -> None:
        """
        put request item from scheduler
        :param request:
        :param callback: call back func
        :return: None
        """
        flag_string = 'cb_decrease_flag'
        if not getattr(callback, flag_string, False):
            callback = call_decrease(self.concurrency)(callback)
            setattr(callback, flag_string, True)

        while not self.empty() and self.concurrency < self.max_concurrency:
            ret = self.get()
            if ret:
                req, cb = ret
                self.downloader.fetch(req, cb)

    def empty(self) -> bool:
        """
        scheduler's queue empty or not
        :return: Boolean, True or False
        """
        pass
