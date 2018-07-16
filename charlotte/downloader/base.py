from typing import Callable
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
        If response fetched, call handle func to handle it.
        :param request: HTTPRequest object
        :param callback: func with HTTPResponse object as arguments
        :return: None
        """
        pass
