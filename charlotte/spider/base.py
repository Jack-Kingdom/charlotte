import logging
import asyncio
from typing import Generator, Callable, Union
from charlotte.scheduler.queue import QueueScheduler
from charlotte.core.http import HTTPRequest, HTTPResponse

logger = logging.getLogger(__name__)


class BaseSpider(object):
    """
    Interface for spider.
    """

    # set QueueScheduler as default
    scheduler = QueueScheduler()

    fetch = scheduler.fetch

    async def on_start(self) -> Generator:
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
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            loop.stop()
            logger.error("received KeyboardInterrupt, spider execute interrupted.")
        else:
            logger.info("spider execute finished.")
