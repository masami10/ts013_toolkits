# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextBrowser
from typing import List
from transport.constants import now
from tools.view.mixin import ToolKitMixin
from loguru import logger


class ToolkitNotify:
    qt_instances: List[QTextBrowser]

    def __init__(self, instances: List[QTextBrowser]):
        self.qt_instances = []
        for instance in instances:
            self.qt_instances.append(instance)

    def _notify(self, color: str, content: str):
        if not self.qt_instances or len(self.qt_instances) == 0:
            return
        data = f'时间:{now()}, 内容: {content}'
        ss = "<span style=\" font-size:16pt; font-weight:600; color:#{};\" > {} </span>".format(color, data)
        for instance in self.qt_instances:
            instance.append(ss)

    def error(self, content: str):
        color = 'e33371'
        self._notify(color, content)
        logger.error(content)

    @staticmethod
    def debug(content: str):
        # color = 'e33371'
        # self._notify(color, content)
        logger.debug(content)

    def info(self, content: str):
        color = '81c784'
        self._notify(color, content)
        logger.info(content)

    def warn(self, content: str):
        color = 'ffb74d'
        self._notify(color, content)
        logger.warning(content)
