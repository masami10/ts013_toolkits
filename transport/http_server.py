from PyQt5 import QtCore
from http import HTTPStatus
from aiohttp import web
from loguru import logger

logger.add("logs/curve_collection_agent.log", rotation="1 days", level="INFO", encoding='utf-8')  # 文件日誌


async def healthzCheckHandler(request):
    return web.Response(status=HTTPStatus.NO_CONTENT)


async def postOrderHandler(request):

    return web.Response(status=HTTPStatus.CREATED)


def create_web_app() -> web.Application:
    # loop = asyncio.get_event_loop()
    ret: web.Application = web.Application(client_max_size=1024 * 1024 * 10)
    ret.add_routes([web.get('/healthz', healthzCheckHandler),
                    web.post('/orders', postOrderHandler),
                    ])

    return ret


class HttpDaemon(object):
    def __init__(self, port=9110, *args, **kwargs):
        super(HttpDaemon, self).__init__(*args, **kwargs)
        self._port = port
        self._app = create_web_app()

    def start(self):
        self.run()

    def run(self):
        logger.info("Http Server Start")
        web.run_app(self._app, host='0.0.0.0', port=self._port, access_log=logger)
        logger.info("Http Server Stop")

    def stop(self):
        self._app.shutdown()
