from tornado.ioloop import IOLoop
from tornado import httpclient



def handle_response(response):
    if response.error:
        print("Error: %s" % response.error)
    else:
        print(response.body)

    IOLoop.current().stop()


http_client = httpclient.AsyncHTTPClient()
http_client.fetch("http://www.baidu.com/", handle_response)


try:
    IOLoop.current().start()
except KeyboardInterrupt:
    IOLoop.current().stop()
