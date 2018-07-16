from typing import Callable
from functools import partial
from tornado.httpclient import HTTPRequest, HTTPResponse


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    request_middleware = ()
    response_middleware = ()

    def fetch(self, request: HTTPRequest, callback: Callable) -> None:
        """
        Load middleware and fetch page.
        You need to implement fetch by extends this func.
        :param request: HTTPRequest object
        :param callback: func with HTTPResponse object as arguments
        :return: None
        """

        for mw in self.request_middleware:
            request = mw(request)

        if not request:
            return None

    def handle(self, response: HTTPResponse, callback: Callable):
        """
        Load middleware and call callback with response objects.
        :param response: HTTPResponse object
        :param callback: func with HTTPResponse object as arguments
        :return: None
        """
        for mw in self.response_middleware:
            response = mw(response)

        if not response:
            return None

        callback(response)
