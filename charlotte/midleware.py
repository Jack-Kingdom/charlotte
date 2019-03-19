import logging
from typing import Union
from charlotte.helper import str2hash
from charlotte.http import HTTPRequest, HTTPResponse

logger = logging.getLogger(__name__)


class BaseMiddleWare(object):

    def __call__(self, item: Union[HTTPRequest, HTTPResponse], *args, **kwargs):
        if isinstance(item, HTTPRequest):
            self.handle_req(item)
        elif isinstance(item, HTTPResponse):
            self.handle_res(item)
        else:
            raise TypeError('item must be HTTPRequest or HTTPResponse object.')

    def handle_req(self, request: HTTPRequest) -> Union[HTTPRequest, None]:
        """
        request handler
        :param request: HTTPRequest object
        :return: HTTPRequest object or None
        """
        pass

    def handle_res(self, response: HTTPResponse) -> Union[HTTPResponse, None]:
        """
        response handler
        :param response: HTTPResponse object
        :return: HTTPResponse object or None
        """
        pass


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

        if response.status_code == 599:  # todo, redesign this status code
            logger.debug('page {0} fetch error, remove from set.'.format(response.request.url))
            self.set.remove(digest)
        return response
