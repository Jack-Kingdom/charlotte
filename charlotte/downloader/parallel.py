import logging
import functools
from tornado import httpclient
from tornado.httpclient import HTTPRequest, HTTPResponse
from ..downloader.base import BaseDownloader
from .. import setting

logger = logging.getLogger(__name__)


class ParallelDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    middleware = ()

    client = httpclient.AsyncHTTPClient(max_clients=setting.max_concurrency)

    def fetch(self, request: HTTPRequest) -> None:
        """
        fetch request and call callback with response
        """

        request = functools.reduce(lambda item, func: func(item), (request, *self.middleware))

        self.client.fetch(request, self.handle)

    def handle(self, response: HTTPResponse):
        """
        handle response and middleware, call callback func
        :param response: HTTPResponse object
        :return: None
        """

        response = functools.reduce(lambda item, func: func(item), (response, *reversed(self.middleware)))

        callback = getattr(response.request, 'callback')
        callback(response)
