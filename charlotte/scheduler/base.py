import logging
from tornado.httpclient import HTTPRequest, HTTPResponse
from ..downloader.base import BaseDownloader
from ..downloader.async import AsyncDownloader
from .. import setting

logger = logging.getLogger(__name__)


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def __init__(self, downloader: BaseDownloader):
        self.downloader = downloader if downloader else AsyncDownloader()
        self.max_concurrency = setting.max_concurrency
        self.concurrency = 0

    def put(self, request: HTTPRequest) -> None:
        """
        put request item from scheduler
        :param request: HTTPRequest object
        :return: None
        """
        pass

    def get(self) -> HTTPRequest:
        """
        get request obj and callback func from scheduler
        :return: HTTPRequest object
        """
        pass

    def fetch(self, request: HTTPRequest):
        """
        wrapper for downloader's fetch method.
        :param request: HTTPRequest object.
        :return: None
        """

        self.concurrency += 1

        setattr(request, 'callback', self.handle)
        self.downloader.fetch(request)

    def handle(self, response: HTTPResponse):
        """
        wrapper for downloader's handle method.
        :param response: HTTPResponse object
        :return: None
        """

        self.concurrency -= 1

        # try maximize downloader's concurrency
        while not self.empty() and self.concurrency < self.max_concurrency:
            self.fetch(self.get())

        # retry if fetch error
        if response.code == 599:
            retry_times = getattr(response.request, 'retry_times', 0)

            if retry_times < setting.max_retry:
                logger.warning('page {0} fetch failed, err: {1}, retry... ({2}/{3})'
                               .format(response.request.url, response.error, retry_times + 1, setting.max_retry))
                setattr(response.request, 'retry_times', retry_times + 1)
                self.put(response.request)
                return None
            else:
                logger.error("page {0} fetch failed. max_retry times tried.".format(response.request.url))
                return None

        logger.info('page {0} fetch success.'.format(response.request.url))
        parser = getattr(response.request, 'parser')
        parser(response)

    def empty(self) -> bool:
        """
        scheduler's queue empty or not
        :return: Boolean, True or False
        """
        pass
