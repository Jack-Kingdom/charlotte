import logging
import asyncio
from typing import Generator
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

    def run(self):
        """
        run spider
        :return: None
        """

        for item in self.start():
            # wrap item to HTTPRequest object
            request = item if isinstance(item, HTTPRequest) else HTTPRequest(url=item)

            if not getattr(request, 'parser', None):
                setattr(request, 'parser', self.parse)

            self.scheduler.put(request)

        # check finished or not
        loop = asyncio.get_event_loop()
        feature = asyncio.Future()
        asyncio.ensure_future(self.is_over(feature))
        try:
            loop.run_until_complete(feature)
        except KeyboardInterrupt:
            logger.error("received KeyboardInterrupt, spider execute interrupted.")
            loop.close()
        else:
            logger.info("spider execute finished.")
