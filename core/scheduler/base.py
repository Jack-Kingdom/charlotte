from tornado.httpclient import HTTPRequest


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def get(self):
        pass

    def put(self, request: HTTPRequest):
        pass

    def empty(self):
        pass
