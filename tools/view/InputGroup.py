# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QWidget
from typing import Dict
from PyQt5 import QtCore
from functools import partial
from loguru import logger

class InputGroup(QWidget):
    inputChanged = QtCore.pyqtSignal(str, str)
    set_test_signal = QtCore.pyqtSignal(str, str)
    _inputs: Dict[str, QLineEdit]

    def __init__(self, instances: Dict[str, QLineEdit]):
        QWidget.__init__(self)
        self._inputs = instances
        for key, instance in self._inputs.items():
            instance.textChanged.connect(partial(self.on_input_changed, key))
        self.set_test_signal.connect(self.render_text)

    def on_input_changed(self, key, value):
        self.inputChanged.emit(key, value)

    def render_text(self, key, text):
        try:
            input = self._inputs.get(key, None)
            if not input:
                raise Exception('不存在输入框：{}'.format(key))
            if not isinstance(text, str):
                text = str(text)
            input.setText(text)
        except Exception as e:
            logger.error(e)

    def set_text(self, key, text):
        self.set_test_signal.emit(key, text)

    def set_texts(self, texts: dict):
        for key, value in texts.items():
            self.set_text(key, value)

