from queue import Queue
from tornado.httpclient import HTTPRequest
from ..scheduler.base import BaseScheduler


class QueueScheduler(BaseScheduler):
    """
    In memory queue scheduler.
    Be careful of memory run out.
    """

    queue = Queue()

    def get(self):
        if not self.empty():
            return self.queue.get_nowait()
        else:
            return None

    def put(self, request: HTTPRequest):

        if self._concurrency < self.max_concurrency:
            self.fetch(request)
        else:
            self.queue.put_nowait(request)

    def empty(self):
        return self.queue.empty()
