import functools
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

        for mw in self.request_middleware:
            request = mw(request)
            if not request:
                return None

        response = await self.client.fetch(request)

        for mw in self.response_middleware:
            response = mw(response)

            if not request:
                return None

            # fetch again
            if isinstance(response, HTTPRequest):
                self.fetch(response, callback)
                return None

        callback(response)
