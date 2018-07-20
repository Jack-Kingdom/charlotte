import logging
from tornado.httpclient import HTTPRequest, HTTPResponse
from .base import BaseMiddleWare

logger = logging.getLogger(__name__)


class URLSetFilter(BaseMiddleWare):
    """
    HTTPRequest filter by set
    """

    def __init__(self):
        self.set = set()

    def handle_req(self, request: HTTPRequest):

        if request.url in self.set:
            logger.debug('page {0} in set, filtered.'.format(request.url))
            return None
        else:
            logger.debug('page {0} add to set.'.format(request.url))
            self.set.add(request.url)
            return request

    def handle_res(self, response: HTTPResponse):
        if response.code == 599:
            logger.debug('page {0} fetch error, remove from set.'.format(response.request.url))
            self.set.remove(response.request.url)
        return response
