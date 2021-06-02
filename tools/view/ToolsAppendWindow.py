# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
from ui.toolkit import Ui_MainWindow
from ui.tools_append_window import Ui_ToolsAppendWindow
from PyQt5.QtCore import QTimer, QDateTime
from .mixin import ToolKitMixin
from tools.view import table, notify, InputGroup, StatusIndicator


class ToolsAppendWindow(ToolKitMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        window = QtWidgets.QMainWindow(*args, **kwargs)
        ToolKitMixin.__init__(self, window)
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_ToolsAppendWindow()
        self.ui.setupUi(self.qt_instance)
        self.tools_append_window = QtWidgets.QMainWindow()
        self.ui.centralwidget.setProperty('class', 'bgLight')
        self.ui.SaveButton.setProperty('class', 'primaryButton')
        self.ui.CancelButton.setProperty('class', 'danger')
        self.input_group = InputGroup.InputGroup({
            'toolFixedInspectionCode': self.ui.InspectionCodeEdit,
            'toolMaterialCode': self.ui.ProductCodeEdit,
            'toolRfid': self.ui.RFIDEdit,
            'toolClassificationCode': self.ui.ClassificationCodeEdit,
            'toolName': self.ui.NameEdit,
            'toolSpecificationType': self.ui.SpecsEdit,
        })
