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
import asyncio
from charlotte.spider import BaseSpider


class Spider(BaseSpider):

    async def on_start(self):
        response = await self.fetch('https://blog.qiaohong.org/api/v1/articles?limit=999')
        items = json.loads(response.body)

        print(len(items))

        await asyncio.wait(
            [self.fetch('https://blog.qiaohong.org/api/v1/articles/' + item['slug'],
                        parser=self.parse_detail) for item in items])

    def parse_detail(self, res):
        print(res.body)


if __name__ == '__main__':
    Spider().run()


```

## Documentation
Check [wiki](https://github.com/Jack-Kingdom/charlotte/wiki) for details.

## LICENSE
MIT