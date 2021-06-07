from zeep import Client, Settings
from loguru import logger
from zeep.cache import SqliteCache
from zeep.transports import Transport
import os
from distutils.util import strtobool
from requests import Response
from http import HTTPStatus
from lxml.etree import tostring
from sqlite3 import Connection
from zeep.wsa import WsAddressingPlugin
from zeep.plugins import HistoryPlugin

from store.contants import TS013_DB_NAME

ENV_DEBUG_WSDL_REQ = strtobool(os.getenv('ENV_DEBUG_WSDL_REQ', 'false'))


class WSDLClient(object):
    _cache = SqliteCache(path='wsdl_cache.db', timeout=30)
    _settings = Settings(strict=False, xml_huge_tree=True, raw_response=True)

    def __init__(self, db_connect: Connection, wsdl_url: str, wsdl_setting=_settings):
        self._wsdl = wsdl_url
        self._setting = wsdl_setting
        self._sqlite_conn = db_connect
        self._client = None
        self._connected = False

    def do_connect(self) -> Client:
        if not self._connected:
            self._client = Client(self._wsdl, settings=self._setting,
                                  transport=Transport(cache=self._cache, timeout=30, operation_timeout=120),
                                  plugins=[WsAddressingPlugin(), HistoryPlugin()])
            self._connected = True
        return self._client

    def __setattr__(self, key, value):
        if key == '_cache':  # cache不允许被赋值
            return
        super(WSDLClient, self).__setattr__(key, value)

    def do_request(self, method: str, data: dict) -> (bool, str):
        client = self.do_connect()
        m = client.service[method]
        if ENV_DEBUG_WSDL_REQ:
            node = client.create_message(self._client.service, method, **data)
            ss = tostring(node, encoding='utf-8', pretty_print=True)
            logger.info(f"发送WSDL数据: {ss}")
        if not m:
            logger.error(f"无法识别到方法： {method}, url: {self._wsdl}")
            return False
        resp: Response = m(**data)
        if resp.status_code >= HTTPStatus.BAD_REQUEST:
            text = f"请求失败: {resp.text}"
            return False, text
        text = f"接收到原始数据：{resp.text}"
        return True, text
