# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QWidget
from typing import Dict
from PyQt5 import QtCore
from functools import partial


class InputGroup(QWidget):
    inputChanged = QtCore.pyqtSignal(str, str)

    def __init__(self, instances: Dict[str, QLineEdit]):
        QWidget.__init__(self)
        for key, instance in instances.items():
            instance.textChanged.connect(partial(self.on_input_changed, key))

    def on_input_changed(self, key, value):
        self.inputChanged.emit(key, value)