import logging
import functools
from tornado import httpclient
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from .. import setting

logger = logging.getLogger(__name__)


class AsyncDownloader(BaseDownloader):
    """
    parallel downloader.
    """

    middleware = ()

    client = httpclient.AsyncHTTPClient(max_clients=setting.max_concurrency)

    async def fetch(self, request: HTTPRequest) -> None:
        """
        fetch request and call callback with response
        """

        request = functools.reduce(lambda item, func: None if not item else func(item),
                                   (request, *self.middleware))

        if not request:
            logger.info('page {0} filtered.'.format(request.url))
            return None

        response = await self.client.fetch(request)

        # retry if fetch error
        if response.code == 599:
            retry_times = getattr(response.request, 'retry_times', 0)

            if retry_times < setting.max_retry:
                logger.warning(
                    'page {0} fetch failed, reason: {1}, retry...'.format(response.request.url, response.reason))
                setattr(response.request, 'retry_times', retry_times + 1)
                self.fetch(response.request)
                return None
            else:
                logger.error("page {0} fetch failed. max_retry times tried.".format(response.request.url))
                return None

        response = functools.reduce(lambda item, func: None if not item else func(item),
                                    (response, *reversed(self.middleware)))

        callback = getattr(response.request, 'callback')
        callback(response)
