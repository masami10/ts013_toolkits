from PyQt5 import QtCore
from aiohttp import web
from http import HTTPStatus
from loguru import logger

logger.add("logs/curve_collection_agent.log", rotation="1 days", level="INFO", encoding='utf-8')  # 文件日誌


async def healthzCheckHandler(request):
    return web.Response(status=HTTPStatus.NO_CONTENT)


def create_web_app() -> web.Application:
    # loop = asyncio.get_event_loop()
    ret: web.Application = web.Application(client_max_size=1024 * 1024 * 10)
    ret.add_routes([web.get('/healthz', healthzCheckHandler)])

    return ret


class HttpDaemon(QtCore.QThread):
    def __init__(self, port=9110, *args, **kwargs):
        super(HttpDaemon, self).__init__(*args, **kwargs)
        self._port = port
        self._app = create_web_app()

    def run(self):
        web.run_app(self._app, host='0.0.0.0', port=self._port, access_log=logger)

    def stop(self):
        self._app.shutdown()
        self.wait()
