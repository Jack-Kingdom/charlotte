import asyncio
import uvloop
from tornado.platform.asyncio import AsyncIOMainLoop

# register uvloop for better performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
AsyncIOMainLoop().instance()
