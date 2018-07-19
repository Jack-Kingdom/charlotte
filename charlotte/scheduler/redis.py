import pickle
from redis import Redis
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from .base import BaseScheduler


class RedisScheduler(BaseScheduler):
    """
    redis scheduler.
    todo ensure request handle finished.
    """

    def __init__(self,
                 redis: Redis = None,
                 downloader: BaseDownloader = None):
        super(RedisScheduler, self).__init__(downloader)
        self.redis = redis

    def get(self):
        if not self.empty():
            return pickle.loads(self.redis.lpop('queue'))
        else:
            return None

    def put(self, request: HTTPRequest):

        if self.concurrency < self.max_concurrency:
            self.fetch(request)
        else:
            self.redis.lpush('queue', pickle.dumps(request))

    def empty(self):
        return not self.redis.llen('queue')
