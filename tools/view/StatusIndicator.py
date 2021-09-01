# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QWidget
from tools.view.mixin import ToolKitMixin
from PyQt5 import QtCore


class StatusIndicator(ToolKitMixin, QWidget):
    successChanged = QtCore.pyqtSignal(str, bool)
    render_status_signal = QtCore.pyqtSignal(bool)
    _success: bool
    _key: str

    def __init__(self, instance: QPushButton, key: str, success_text='成功', fail_test='失败', disabled=False):
        ToolKitMixin.__init__(self, instance)
        QWidget.__init__(self)
        self._key = key
        self._success_text = success_text
        self._fail_test = fail_test
        self._disabled = disabled
        self.qt_instance.setProperty('class', 'resultButton')
        self.qt_instance.setStyleSheet("")
        self.set_success()
        self.qt_instance.clicked.connect(self.on_clicked)
        self.render_status_signal.connect(self.render_status)

    def set_success(self, success=True):
        self._success = success
        self.render_status_signal.emit(self._success)

    def render_status(self, success: bool):
        text = self._success_text if success else self._fail_test
        self.qt_instance.setProperty('text', text)
        class_name = 'resultButton resultButtonSuccess' if success else 'resultButton resultButtonFailed'
        self.qt_instance.setProperty('class', class_name)
        self.qt_instance.style().polish(self.qt_instance)

    def on_clicked(self):
        if self._disabled:
            return
        self.set_success(success=not self._success)
        self.successChanged.emit(self._key, self._success)
