from typing import Callable
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from .. import setting


class AsyncDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    client = httpclient.AsyncHTTPClient(max_clients=setting.max_concurrency)

    async def fetch(self, request: HTTPRequest, callback: Callable) -> None:
        """
        fetch request and return response
        """
        super(AsyncDownloader, self).fetch(request, callback)

        response = await self.client.fetch(request)
        self.handle(response, callback)
