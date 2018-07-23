import pickle
from redis import Redis
from tornado.httpclient import HTTPRequest
from ..downloader.base import BaseDownloader
from .base import BaseScheduler

# mapper for string and parser func
# loads & dumps func used to avoid pickle dump too deep.
func_map = {}


def loads(bs: bytes) -> HTTPRequest:
    """
    loads bytes to HTTPRequest, add some attr
    :param bs: bytes
    :return: HTTPRequest objects
    """

    request = pickle.loads(bs)

    name = getattr(request, 'name')
    spider_map = func_map[name]

    parser_name = getattr(request, 'parser')
    parser = spider_map[parser_name]
    setattr(request, 'parser', parser)
    return request


def dumps(request: HTTPRequest) -> bytes:
    """
    dump HTTPRequest to bytes, remove some unused reference.
    :param request: HTTPRequest objects
    :return: bytes
    """
    name = getattr(request, 'name')

    if name not in func_map:
        func_map[name] = {}
    spider_map = func_map[name]

    parser = getattr(request, 'parser')
    parser_name = str(parser).split(' ')[1]
    setattr(request, 'parser', parser_name)
    spider_map[parser_name] = parser
    return pickle.dumps(request)


class RedisScheduler(BaseScheduler):
    """
    redis scheduler.
    """

    def __init__(self,
                 redis: Redis = None,
                 downloader: BaseDownloader = None,
                 middleware: tuple = None):
        super(RedisScheduler, self).__init__(downloader, middleware)
        self.redis = redis

    def get(self):

        name = getattr(self, 'name')
        queue = '{0}-queue'.format(name)

        if not self.empty():
            return loads(self.redis.lpop(queue))
        else:
            return None

    def put(self, request: HTTPRequest):

        name = getattr(self, 'name')
        queue = '{0}-queue'.format(name)

        if self.concurrency < self.max_concurrency:
            self.fetch(request)
        else:
            self.redis.lpush(queue, dumps(request))

    def empty(self):

        name = getattr(self, 'name')
        queue = '{0}-queue'.format(name)

        return not self.redis.llen(queue)
