# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QWidget
from typing import Dict
from PyQt5 import QtCore
from functools import partial


class InputGroup(QWidget):
    inputChanged = QtCore.pyqtSignal(str, str)

    _inputs: Dict[str, QLineEdit]

    def __init__(self, instances: Dict[str, QLineEdit]):
        QWidget.__init__(self)
        self._inputs = instances
        for key, instance in self._inputs.items():
            instance.textChanged.connect(partial(self.on_input_changed, key))

    def on_input_changed(self, key, value):
        self.inputChanged.emit(key, value)

    def set_text(self, key, text):
        input = self._inputs.get(key, None)
        if not input:
            raise Exception('不存在输入框：{}'.format(key))
        input.setText(text)
