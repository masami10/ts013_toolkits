# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QWidget
from tools.view.mixin import ToolKitMixin
from PyQt5 import QtCore
from loguru import logger


class ResultButton(ToolKitMixin, QWidget):
    successChanged = QtCore.pyqtSignal(str, bool)
    _success: bool
    _key: str

    def __init__(self, instance: QPushButton, key: str):
        ToolKitMixin.__init__(self, instance)
        QWidget.__init__(self)
        self._key = key
        self.qt_instance.setProperty('class', 'resultButton')
        self.qt_instance.setStyleSheet("")
        self.set_success()
        self.qt_instance.clicked.connect(self.on_clicked)

    def set_success(self, success=True):
        self._success = success
        text = '成功' if success else '失败'
        self.qt_instance.setProperty('text', text)
        class_name = 'success resultButton resultButtonSuccess' if success else 'danger resultButton resultButtonFailed'
        self.qt_instance.setProperty('class', class_name)
        self.qt_instance.style().polish(self.qt_instance)

    def on_clicked(self):
        self.set_success(success=not self._success)
        self.successChanged.emit(self._key, self._success)
