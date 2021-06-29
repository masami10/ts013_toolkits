from PyQt5 import QtCore
from http import HTTPStatus
from aiohttp import web
from loguru import logger
import sqlite3
from sqlite3 import Connection
from store.contants import TS013_DB_NAME
from store.sql import insert_ts013_order_item
from transport.constants import local_datetime_from_str


async def healthzCheckHandler(req):
    return web.Response(status=HTTPStatus.NO_CONTENT)


async def postOrderHandler(req):
    payload = await req.json()
    app = req.app
    if not app.get('database'):
        app['database'] = sqlite3.connect(TS013_DB_NAME)
    try:
        db: Connection = app['database']
        if not db:
            raise Exception('请初始化数据库接口')
        entry = payload.get('resultInfo') or payload.get('requestInfo')
        if not entry:
            raise Exception('没有找到订单数据入口')
        orderinfo = entry.get('MOMWIPORDER')
        operationInfo = orderinfo.get('MOMWIPORDEROPR', {})
        ordername = orderinfo.get('WIPORDERNO')
        workcenter = operationInfo.get('WORKCENTER', '')
        schedule_date_time = local_datetime_from_str(orderinfo.get('SCHEDULEDSTARTDATE'))
        rid = insert_ts013_order_item(db, ordername, orderinfo.get('WIPORDERTYPE'),
                                      schedule_date_time,
                                      orderinfo.get('PRODUCTNO'),
                                      workcenter
                                      )
        if rid < 0:
            raise Exception('订单插入数据库错误')
        logger.info(f'订单: {ordername} 插入数据库成功')
        db.commit()
        return web.Response(status=HTTPStatus.CREATED)
    except Exception as e:
        msg = f"postOrderHandler error: {e}"
        logger.error(msg)
        return web.Response(status=HTTPStatus.BAD_REQUEST, text=msg)


def create_web_app() -> web.Application:
    # loop = asyncio.get_event_loop()
    ret: web.Application = web.Application(client_max_size=1024 * 1024 * 10)
    ret.add_routes([web.get('/healthz', healthzCheckHandler),
                    web.post('/ts013/workorders', postOrderHandler),
                    ])

    return ret


class HttpServer(object):
    def __init__(self, port=9110, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)
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
