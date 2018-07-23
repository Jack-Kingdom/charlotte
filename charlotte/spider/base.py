import logging
import asyncio
from typing import Generator, Callable, Union
from tornado.httpclient import HTTPRequest, HTTPResponse
from ..scheduler import QueueScheduler

logger = logging.getLogger(__name__)


class BaseSpider(object):
    """
    Interface for spider.
    """

    # set QueueScheduler as default
    scheduler = QueueScheduler()

    def start(self) -> Generator:
        """
        Spider start function. Call once on spider start.
        :return: a generator of tuple, HTTPRequest object and callback func
        """
        pass

    def parse(self, response: HTTPResponse) -> Generator:
        """
        Default parse function.
        :param response:
        :return:
        """
        pass

    async def is_over(self, feature: asyncio.Future):
        while True:
            await asyncio.sleep(0.1)
            if self.scheduler.empty() and self.scheduler.concurrency == 0:
                feature.set_result('Feature is done!')

    def fetch(self, req: Union[str, HTTPRequest], parser: Callable = None) -> None:
        """
        wrap request url or HTTPRequest objects with some additional attr
        :param req: request url or HTTPRequest objects
        :param parser: optional arguments, parse func
        :return: None
        """

        # wrap item to HTTPRequest object
        request = req if isinstance(req, HTTPRequest) else HTTPRequest(url=req)

        # flag request with spider name
        setattr(request, 'name', getattr(self, 'name'))

        # if no appointed parser, self.parse func as default.
        if not getattr(request, 'parser', None):
            setattr(request, 'parser', self.parse)

        self.scheduler.put(request)

    def run(self):
        """
        run spider
        :return: None
        """

        # get spider name, use class name instead if none
        name = getattr(self, 'name', None)
        if not name:
            name = str(self).replace('<', '').split(' ')[0]
            setattr(self, 'name', name)

        # flag scheduler belong to what spider
        setattr(self.scheduler, 'name', name)

        # handle start func generated request
        for item in self.start():
            self.fetch(item)

        # check finished or not
        loop = asyncio.get_event_loop()
        feature = asyncio.Future()
        asyncio.ensure_future(self.is_over(feature))
        try:
            loop.run_until_complete(feature)
        except KeyboardInterrupt:
            loop.stop()
            logger.error("received KeyboardInterrupt, spider execute interrupted.")
        else:
            logger.info("spider execute finished.")
