# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTextBrowser
from tools.view.mixin import ToolKitMixin
from loguru import logger


class ToolkitNotify(ToolKitMixin):
    def __init__(self, instance: QTextBrowser):
        super(ToolkitNotify, self).__init__(instance)

    @property
    def textBrowser_instance(self) -> QTextBrowser:
        return self.qt_instance

    def _notify(self, color: str, content: str):
        if not self.textBrowser_instance:
            return
        ss = "<span style=\" font-size:16pt; font-weight:600; color:#{};\" > {} </span>".format(color, content)
        self.textBrowser_instance.append(ss)

    def error(self, content: str):
        color = 'e33371'
        self._notify(color, content)
        logger.error(content)

    def info(self, content: str):
        color = '81c784'
        self._notify(color, content)
        logger.info(content)

    def warn(self, content: str):
        color = 'ffb74d'
        self._notify(color, content)
        logger.warning(content)
