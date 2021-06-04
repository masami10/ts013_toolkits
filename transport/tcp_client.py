import socket
import threading
from typing import Optional, Callable
import time
import platform
import os
from loguru import logger
from distutils.util import strtobool

ENV_KEEPALIVE_ENABLE = strtobool(os.getenv('ENV_KEEPALIVE_ENABLE', 'true'))


class TcpClient(object):

    def __init__(self, ip: str = '127.0.0.1', port: int = 80, name='Dummy TCP Client', newline='\n'):
        self.started = False
        self.connected = False  # 是否连接
        self.start_task = None
        self._name = name
        self._newline = newline
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.RLock()
        self.handler: Optional[Callable[[str], None]] = None
        self._server_addr = (ip, int(port))
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        if not self._server_addr:
            raise Exception('Server Address Is Empty')
        if not self._client:
            raise Exception('Client Is Empty')
        if self.connected:
            raise Exception('连接已存在')
        self._client.settimeout(2.0)  # 设置2秒timeout
        if ENV_KEEPALIVE_ENABLE and platform.system() == 'Windows':
            self._client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 5000, 1000))  # 正常连接时候5s一次，没有的时候1秒一次，最多5次
        self._client.connect(self._server_addr)
        self.connected = True
        return True

    def disconnect(self):
        if not self._client:
            return
        self._client.close()
        self.connected = False

    def set_handler(self, handler: Callable[[str], None]):
        with self._lock:
            self.handler = handler

    def run(self):
        f = self._client.makefile('r', encoding='utf-8', newline=self._newline)
        while self.started:
            if not self.connected:
                logger.info("等待连接")
                time.sleep(0.5)
                continue
            line = f.readline()
            if isinstance(line, bytes):
                line = line.decode(encoding='utf-8')
            line = line.split(self._newline)[0]
            logger.debug(f"接收到数据{line}")
            if self.handler:
                self.handler(line)
        f.close()

    # def do_connect(self):
    #     result = run_and_get_result(self.connect())
    #     return result

    def _do_start(self, on_start, notify):
        notify.info("TCP 客户端启动中...")
        self.connect()
        self.started = True
        self.thread = threading.Thread(target=self.run, name=self._name)
        self.thread.setDaemon(True)
        self.thread.start()
        notify.info("TCP 客户端线程打开")
        on_start()

    def start(self, on_start, notify):
        # if self.start_task:
        #     self.start_task.close()
        self._do_start(on_start, notify)

    def stop(self):
        if self.start_task:
            self.start_task.close()
        self.started = False
        self.disconnect()
        if self.thread:
            self.thread.join()
        logger.info("TCP 客户端线程关闭")
