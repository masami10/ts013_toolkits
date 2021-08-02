# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QRadioButton, QWidget
from PyQt5 import QtCore


class CheckTypeRadio(QWidget):
    checkTypeChanged = QtCore.pyqtSignal(bool)

    def __init__(self, first_check_instance: QRadioButton, recheck_instance: QRadioButton):
        QWidget.__init__(self)
        first_check_instance.clicked.connect(self.on_first_check_clicked)
        recheck_instance.clicked.connect(self.on_recheck_clicked)

    def on_first_check_clicked(self):
        self.checkTypeChanged.emit(True)

    def on_recheck_clicked(self):
        self.checkTypeChanged.emit(False)

