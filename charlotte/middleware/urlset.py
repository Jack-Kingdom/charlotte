import logging
import hashlib
from tornado.httpclient import HTTPRequest, HTTPResponse
from .base import BaseMiddleWare

logger = logging.getLogger(__name__)


def to_hash(url: str) -> str:
    """
    hash url
    :param url: url string
    :return: hex digest
    """
    url = url.encode('utf-8')

    return hashlib.sha256(url).hexdigest()


class URLSetFilter(BaseMiddleWare):
    """
    HTTPRequest filter by set
    """

    def __init__(self):
        self.set = set()

    def handle_req(self, request: HTTPRequest):

        digest = to_hash(request.url)

        if digest in self.set:
            logger.debug('page {0} in set, filtered.'.format(request.url))
            return None
        else:
            logger.debug('page {0} add to set.'.format(request.url))
            self.set.add(digest)
            return request

    def handle_res(self, response: HTTPResponse):

        digest = to_hash(response.request.url)

        if response.code == 599:
            logger.debug('page {0} fetch error, remove from set.'.format(response.request.url))
            self.set.remove(digest)
        return response
