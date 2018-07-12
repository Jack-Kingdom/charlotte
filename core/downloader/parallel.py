from typing import Callable
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from core.downloader.base import BaseDownloader


class ParallelDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    def __init__(self):
        self.client = httpclient.AsyncHTTPClient()

    def fetch(self, request: HTTPRequest, callback: Callable) -> None:
        """
        fetch request and return response
        """

        self.client.fetch(request, callback)
