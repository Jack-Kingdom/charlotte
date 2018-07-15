from queue import Queue
from typing import Callable
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from ..scheduler.base import BaseScheduler


class QueueScheduler(BaseScheduler):
    """
    In memory queue scheduler.
    Be careful of memory run out.
    """

    def __init__(self, downloader: BaseDownloader):
        super(QueueScheduler, self).__init__(downloader)
        self.queue = Queue()

    def get(self):
        if not self.queue.empty():
            return self.queue.get_nowait()
        else:
            return None

    def put(self, request: HTTPRequest, callback: Callable):

        super(QueueScheduler, self).put(request, callback)

        if self.concurrency < self.max_concurrency:
            self.downloader.fetch(request, callback)
        else:
            self.queue.put_nowait((request, callback))

    def empty(self):
        return self.queue.empty()
