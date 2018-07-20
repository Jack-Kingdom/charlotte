from typing import Union
from tornado.httpclient import HTTPRequest, HTTPResponse


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
