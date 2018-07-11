from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado.httpclient import HTTPRequest, HTTPResponse
from core.schedule import BaseScheduler
from . import setting


class BaseSpider(object):
    def __init__(self, scheduler: BaseScheduler = None):
        self.scheduler = scheduler
        self.concurrency = 0

    def before(self):
        for _ in range(setting.max_concurrency):
            self.scheduler.put(HTTPRequest(url="http://blog.qiaohong.com/"))

    def start(self):
        http_client = httpclient.AsyncHTTPClient()
        while not self.scheduler.empty():
            request = self.scheduler.get()
            http_client.fetch(request, self.parse)

    @staticmethod
    def parse(response: HTTPResponse):
        if response.error:
            print("Error:", response.error)
        else:
            print("Body:", response.body)

    def run(self):
        IOLoop.current().start()
