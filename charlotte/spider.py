import typing
import logging
import asyncio
import functools
from charlotte.helper import url2request
from charlotte.fetch import fetch_request
from charlotte.http import HTTPRequest, HTTPResponse

logger = logging.getLogger(__name__)


class BaseSpider(object):
    """
    Interface for Scheduler class
    """

    name = "base_spider"    # used to format logging print
    default_loop = asyncio.get_event_loop()
    middleware = ()
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

    def fetch(self, request: typing.Union[HTTPRequest, str], parser=None) -> \
            typing.Union[asyncio.Future, typing.Coroutine, None]:
        """
        wrapper for downloader's fetch method.
        :param request: HTTPRequest object.
        :param parser: callback for http response
        :return: HTTPResponse if without parser else None
        """

        # load middleware
        request = self._load_mw(request if isinstance(request, HTTPRequest) else url2request(request))
        if not request:
            logger.info('request {0} filtered by middleware.'.format(request.uri))
            return None  # todo await None ?

        task = fetch_request(request, loop=self.default_loop)

        if parser:
            return self.after_fetch(task, parser)
        else:
            return task

        # future = asyncio.wait(self.pending, loop=self.default_loop)
        # return future

    async def after_fetch(self, task, callback):
        response = self._load_mw(await task)
        if response:
            callback(response)
        else:
            logger.info("request filtered by middleware.")

    async def on_start(self):
        """
        Spider start function. Call once on spider start.
        :return: a generator of tuple, HTTPRequest object and callback func
        """
        pass

    def run(self):
        """
        run spider
        :return: None
        """

        task = self.on_start()
        try:
            self.default_loop.run_until_complete(asyncio.wait([task]))
        except KeyboardInterrupt:
            self.default_loop.stop()
            logger.error("received KeyboardInterrupt, spider execute interrupted.")
        else:
            logger.info("spider execute finished.")
