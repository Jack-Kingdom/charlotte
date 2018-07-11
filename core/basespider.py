from tornado.ioloop import IOLoop
from tornado import httpclient
from tornado.httpclient import HTTPRequest, HTTPResponse
from core.schedule import BaseScheduler, QueueScheduler
from . import setting


class BaseSpider(object):
    def __init__(self, scheduler: BaseScheduler = None):
        self.scheduler = scheduler if scheduler else QueueScheduler()

        self.before()
        self.start()

    def start(self):
        http_client = httpclient.AsyncHTTPClient()
        while not self.scheduler.empty():
            request = self.scheduler.get()
            http_client.fetch(request, self.parse)

    def before(self):
        for _ in range(100000):
            self.scheduler.put(HTTPRequest(url="http://www.baidu.com/"))

    @staticmethod
    def parse(response: HTTPResponse):
        if response.error:
            print("Error:", response.error)
        else:
            print("Body:", response.body)

    def run(self):
        IOLoop.current().start()
