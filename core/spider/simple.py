from tornado import httpclient
from tornado.httpclient import HTTPRequest, HTTPResponse
from core.scheduler.base import BaseScheduler
from core.spider.base import BaseSpider


class SimpleSpider(BaseSpider):

    def __init__(self, scheduler: BaseScheduler = None):
        super(SimpleSpider, self).__init__(scheduler)

    def start(self):
        http_client = httpclient.AsyncHTTPClient()
        while not self.scheduler.empty():
            request = self.scheduler.get()
            http_client.fetch(request, self.parse)

    def parse(self, response: HTTPResponse):
        if response.error:
            yield ("Error:", response.error)
        else:
            yield ("Body:", response.body)
