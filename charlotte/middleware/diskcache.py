import logging
from tornado.httpclient import HTTPRequest, HTTPResponse
from .base import BaseMiddleWare

logger = logging.getLogger(__name__)


class DiskCache(BaseMiddleWare):

    def __init__(self, folder: str = '.diskcache', timeout=24 * 60 * 60):
        pass

    def handle_req(self, request: HTTPRequest):
        pass

    def handle_res(self, response: HTTPResponse):
        pass
