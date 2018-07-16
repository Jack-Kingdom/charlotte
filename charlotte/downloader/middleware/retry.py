import logging
from tornado.httpclient import HTTPResponse
from ... import setting

logger = logging.getLogger(__name__)


def retry(response: HTTPResponse):
    if response.code == 599:
        retry_times = getattr(response.request, 'retry_times', 0)

        if retry_times < setting.max_retry:
            logger.warning('page {0} fetch failed, reason: {1}, retry...'.format(response.request.url, response.reason))
            setattr(response.request, 'retry_times', retry_times + 1)
            return response.request
        else:
            logger.error("page {0} fetch failed. max_retry times tried.".format(response.request.url))
