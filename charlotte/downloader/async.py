from typing import Callable
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from .. import setting


class AsyncDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    def __init__(self):
        self.client = httpclient.AsyncHTTPClient(max_clients=setting.max_concurrency)

    def fetch(self, request: HTTPRequest, callback: Callable) -> None:
        """
        fetch request and return response
        """

        self.client.fetch(request, callback)
