import logging
from charlotte.core.helper import str2hash
from charlotte.core.http import HTTPRequest, HTTPResponse
from .base import BaseMiddleWare

logger = logging.getLogger(__name__)


class URLSetFilter(BaseMiddleWare):
    """
    HTTPRequest filter by set
    """

    def __init__(self):
        self.set = set()

    def handle_req(self, request: HTTPRequest):

        digest = str2hash(request.uri)

        if digest in self.set:
            logger.debug('page {0} in set, filtered.'.format(request.uri))
            return None
        else:
            logger.debug('page {0} add to set.'.format(request.uri))
            self.set.add(digest)
            return request

    def handle_res(self, response: HTTPResponse):

        digest = str2hash(response.request.uri)

        if response.status_code == 599:    # todo, redesign this status code
            logger.debug('page {0} fetch error, remove from set.'.format(response.request.url))
            self.set.remove(digest)
        return response
