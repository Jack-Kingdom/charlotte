# register uvloop for better performance

try:
    import uvloop
except ImportError as e:
    import logging
    logging.info("you can install uvloop for better performance.")
else:
    import asyncio
    from tornado.platform.asyncio import AsyncIOMainLoop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    AsyncIOMainLoop().instance()
