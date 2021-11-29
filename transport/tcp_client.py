import socket
import threading
from typing import Optional, Callable
import time
import io
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
        self.on_client_status = None
        self._name = name
        self._newline = newline
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.handler: Optional[Callable[[str], None]] = None
        self._server_addr = (ip, int(port))
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, on_start, notify):
        self._lock.acquire()
        try:
            if not self._server_addr:
                raise Exception('Server Address Is Empty')
            if not self._client:
                raise Exception('Client Is Empty')
            if self.connected:
                raise Exception('连接已存在')
            if ENV_KEEPALIVE_ENABLE and platform.system() == 'Windows':
                self._client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 5000, 1000))  # 正常连接时候5s一次，没有的时候1秒一次，最多5次
            self._client.connect(self._server_addr)
            self.connected = True
            notify.info("TCP 客户端线程打开")
            on_start(True)
            self.started = True
        finally:
            self._lock.release()
        try:
            self.run()
        except Exception as e:
            notify.error(e)


    def disconnect(self):
        if not self.connected:
            return
        self._client.shutdown(socket.SHUT_RDWR)
        self.connected = False

    def set_handler(self, handler: Callable[[str], None]):
        self.handler = handler

    def run(self):
        with self._client.makefile('r', encoding='utf-8', newline=self._newline) as f:
            while self.started:
                if not self.connected:
                    logger.info("等待连接")
                    time.sleep(0.5)
                    continue
                try:
                    line = f.readline()
                except Exception as e:
                    # logger.error(e)
                    continue
                if not line:
                    logger.info("客户端断开，请重新连接")
                    self.do_stop()
                    return
                if isinstance(line, bytes):
                    line = line.decode(encoding='utf-8')
                line = line.split(self._newline)[0]
                logger.debug(f"接收到数据{line}")
                if self.handler:
                    self._lock.acquire()
                    try:
                        self.handler(line)
                    finally:
                        self._lock.release()
        # f.close()

    def _do_start(self, on_start, notify):
        notify.info("TCP 客户端启动中...")
        self.thread = threading.Thread(target=self.connect, args=(on_start, notify,), name=self._name)
        self.thread.setDaemon(True)
        self.thread.start()

    def start(self, on_start, notify):
        if self.connected:
            notify.info('tcp已连接')
            return
        self.on_client_status = on_start
        self._do_start(on_start, notify)

    def do_stop(self):
        self.started = False
        self.disconnect()
        if self.on_client_status:
            self.on_client_status(False)

    def stop(self):
        self.do_stop()
        if self.thread.is_alive():
            self.thread.join()
        logger.info("TCP 客户端线程关闭")
