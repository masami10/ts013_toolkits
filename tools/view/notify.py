# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextBrowser, QWidget
from typing import List
from transport.constants import now
from loguru import logger
from PyQt5 import QtCore


class ToolkitNotify(QWidget):
    qt_instances: List[QTextBrowser]
    notify_append_signal = QtCore.pyqtSignal(str)

    def __init__(self, instances: List[QTextBrowser]):
        QWidget.__init__(self)
        self.qt_instances = []
        for instance in instances:
            self.qt_instances.append(instance)
        self.notify_append_signal.connect(self.handle_notify_append)

    def handle_notify_append(self, content: str):
        for instance in self.qt_instances:
            instance.append(content)
            instance.verticalScrollBar().setValue(instance.verticalScrollBar().maximum())

    def _notify(self, color: str, content: str):
        if not self.qt_instances or len(self.qt_instances) == 0:
            return
        data = f'时间:{now()}, 内容: {content}'
        ss = "<span style=\" font-size:10pt; font-weight:600; color:#{};\" > {} </span>".format(color, data)
        self.notify_append_signal.emit(ss)

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
