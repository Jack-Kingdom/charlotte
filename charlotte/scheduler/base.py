import typing
import logging
import asyncio
import functools
from charlotte import setting
from charlotte.core.loop import default_loop
from charlotte.core.fetch import fetch_request
from charlotte.core.http import HTTPRequest, HTTPResponse

logger = logging.getLogger(__name__)


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    middleware = ()
    max_concurrency = setting.default_max_concurrency
    concurrency = 0
    pending = []

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

    def empty(self) -> bool:
        """
        scheduler's crawl jobs empty or not, used to judge spider running status
        :return: Boolean, True or False
        """
        pass

    def _load_mw(self, conn: typing.Union[HTTPRequest, HTTPResponse]) -> typing.Union[HTTPRequest, HTTPResponse, None]:
        """
        load request or response mw
        :param conn: req or res
        :return: req, res or None
        """

        if isinstance(conn, HTTPRequest):
            return functools.reduce(lambda req, mw: None if not req else mw.handle_req(req), (conn, *self.middleware))
        elif isinstance(conn, HTTPResponse):
            return functools.reduce(lambda res, mw: None if not res else mw.handle_res(res), (conn, *self.middleware))
        else:
            raise ValueError("argument conn illegal.")

    def fetch(self, request: HTTPRequest, parser=None) -> typing.Union[asyncio.Future, HTTPResponse, None]:
        """
        wrapper for downloader's fetch method.
        :param request: HTTPRequest object.
        :param parser: callback for http response
        :return: HTTPResponse if without parser else None
        """

        # load middleware
        request = self._load_mw(request)
        if not request:
            logger.info('request {0} filtered by middleware.'.format(request.uri))
            return None

        task = fetch_request(request)

        if parser:
            self.pending.append(self.after_fetch(task, parser))
        else:
            self.pending.append(task)

        future = asyncio.wait(self.pending, loop=default_loop)
        return future

    async def handle(self, response: HTTPResponse, parser=None):
        """
        wrapper for downloader's handle method.
        :param response: HTTPResponse object
        :param parser: callback function
        :return: None
        """

        self.concurrency -= 1

        # load middleware
        response = self._load_mw(response)

        # try maximize downloader's concurrency
        while not self.empty() and self.concurrency < self.max_concurrency:
            self.fetch(self.get())

        # retry if fetch error
        # if response.code == 599:
        #     retry_times = getattr(response.request, 'retry_times', 0)
        #
        #     if retry_times < setting.max_retry:
        #         logger.warning('page {0} fetch failed, err: {1}, retry... ({2}/{3})'
        #                        .format(response.request.url, response.error, retry_times + 1, setting.max_retry))
        #         setattr(response.request, 'retry_times', retry_times + 1)
        #         self.put(response.request)
        #         return None
        #     else:
        #         logger.error("page {0} fetch failed. max_retry times tried.".format(response.request.url))
        #         return None

        logger.info('page {0} fetch success.'.format(response.request.url))

        if parser:
            return parser(response)
        else:
            return response

    async def after_fetch(self, task, callback):
        response = self._load_mw(await task)
        if response:
            callback(response)
        else:
            logger.info("request filtered by middleware.")
