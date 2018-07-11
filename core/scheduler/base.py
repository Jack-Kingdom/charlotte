from tornado.httpclient import HTTPRequest


class BaseScheduler(object):
    """
    Interface for Scheduler class
    """

    def get(self) -> HTTPRequest:
        """
        get request item from scheduler
        :return: HTTPRequest Object
        """
        pass

    def put(self, request: HTTPRequest) -> None:
        """
        put request item from scheduler
        :param request:
        :return: None
        """
        pass

    def empty(self) -> bool:
        """
        scheduler's queue empty or not
        :return: Boolean, True or False
        """
        pass
