from queue import Queue
from tornado.httpclient import HTTPRequest


class BaseScheduler(object):
    def get(self):
        pass

    def put(self, request: HTTPRequest):
        pass


class QueueScheduler(BaseScheduler):
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

    def should_close(self):
        pass
