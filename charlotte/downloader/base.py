from tornado.httpclient import HTTPRequest


class BaseDownloader(object):
    """
    Interface for Downloader
    """

    middleware = ()

    def fetch(self, request: HTTPRequest) -> None:
        """
        Load middleware and fetch page.
        You need to implement fetch by extends this func.
        :param request: HTTPRequest object
        :return: None
        """
        pass
