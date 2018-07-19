# charlotte

[![Build Status](https://travis-ci.com/Jack-Kingdom/charlotte.svg?branch=master)](https://travis-ci.com/Jack-Kingdom/charlotte)

Lightweight and expandable spider framework.

## Install
```shell
pip install charlotte
```

## Example

```python
import json
from tornado.httpclient import HTTPRequest, HTTPResponse
from charlotte.spider import BaseSpider


class BlogSpider(BaseSpider):

    def start(self):
        yield "https://blog.qiaohong.org/api/v1/articles"

    def parse(self, response):
        lst = json.loads(response.body)

        for item in lst:
            request = HTTPRequest("https://blog.qiaohong.org/api/v1/articles" + "/" + item['slug'])
            setattr(request, 'parser', self.parse_detail)

            self.scheduler.put(request)

    def parse_detail(self, response: HTTPResponse):
        detail = json.loads(response.body)
        print(detail)


if __name__ == '__main__':
    BlogSpider().run()
```

## Documentation
Check [wiki](https://github.com/Jack-Kingdom/charlotte/wiki) for details.

## LICENSE
MIT