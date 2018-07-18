from tornado.httpclient import HTTPRequest, HTTPResponse


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    # downloader's middleware focused on patch request & response
    # don't support filter request & response
    middleware = ()

    def fetch(self, request: HTTPRequest) -> None:
        """
        Load middleware and fetch page.
        You need to implement fetch by extends this func.
        :param request: HTTPRequest object
        :return: None
        """
        pass

    def handle(self, response: HTTPResponse):
        """
        handle response and middleware, call callback func
        :param response: HTTPResponse object
        :return: None
        """
        pass
