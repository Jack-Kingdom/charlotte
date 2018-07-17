import time
from typing import Callable, Tuple
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from ..utils.call import call_increase, call_decrease
from .. import setting


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def __init__(self, downloader: BaseDownloader):
        self.downloader = downloader
        self.max_concurrency = setting.max_concurrency
        self.concurrency = 0

        # increase concurrency when fetch func called
        flag_string = 'cb_increase_flag'
        if not getattr(self.downloader.fetch, flag_string, False):
            self.downloader.fetch = call_increase(self.concurrency)(self.downloader.fetch)
            setattr(self.downloader.fetch, flag_string, True)

    def get(self) -> HTTPRequest:
        """
        get request obj and callback func from scheduler
        :return: HTTPRequest object
        """
        pass

    def put(self, request: HTTPRequest) -> None:
        """
        put request item from scheduler
        :param request:
        :return: None
        """
        flag_string = 'cb_decrease_flag'
        if not getattr(getattr(request, 'callback'), flag_string, False):
            callback = call_decrease(self.concurrency)(getattr(request, 'callback'))
            setattr(callback, flag_string, True)

        while not self.empty() and self.concurrency < self.max_concurrency:
            self.downloader.fetch(self.get())

    def empty(self) -> bool:
        """
        scheduler's queue empty or not
        :return: Boolean, True or False
        """
        pass
