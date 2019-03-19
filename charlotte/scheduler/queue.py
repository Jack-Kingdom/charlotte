from queue import Queue
from charlotte.core.http import HTTPRequest
from charlotte.scheduler.base import BaseScheduler


class QueueScheduler(BaseScheduler):
    """
    In memory queue scheduler.
    """

    queue = Queue()

    def get(self):
        if not self.empty():
            return self.queue.get_nowait()
        else:
            return None

    def put(self, request: HTTPRequest):

        if self.concurrency < self.max_concurrency:
            self.fetch(request)
        else:
            self.queue.put_nowait(request)

    def empty(self):
        return self.queue.empty() and self.concurrency == 0
