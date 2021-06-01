# -*- coding:utf-8 -*-
from loguru import logger
from tools.controller.AppController import AppController
import os
import sys
import traceback
import platform

logger.add("logs/curve_toolkit.log", rotation="1 days", level="INFO", encoding='utf-8')  # 文件日誌
# logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

logger.info('系统启动！！！')

app_controller = AppController()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(tb)


sys.excepthook = excepthook

app_controller.run_app()
