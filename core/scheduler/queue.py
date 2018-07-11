from queue import Queue
from tornado.httpclient import HTTPRequest
from .base import BaseScheduler


class QueueScheduler(BaseScheduler):
    """
    In memory queue scheduler.
    Be careful of memory run out.
    """
    def __init__(self):
        self.queue = Queue()

    def get(self):
        if not self.queue.empty():
            return self.queue.get_nowait()
        else:
            return None

    def put(self, request: HTTPRequest):
        self.queue.put_nowait(request)

    def empty(self):
        return self.queue.empty()
