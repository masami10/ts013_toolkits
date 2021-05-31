# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
from ui.toolkit import Ui_MainWindow
from loguru import logger
from typing import Dict, List, Any
from tools.view import table, notify, InputGroup, ResultButton, StatusIndicator
from transport.http_server import HttpDaemon

demo_table_items = [["006R_1_1_1", "2", "3"], ["006R_1_1_2", "22", "342"]]


class ToolKitWindow(QtWidgets.QMainWindow):

    def show(self) -> None:
        super(ToolKitWindow, self).show()
        if self._http_server:
            self._http_server.start()

    def closeEvent(self, event):
        if self._http_server:
            self._http_server.stop()

    def __init__(self, http_server: HttpDaemon, *args, **kwargs):
        super(ToolKitWindow, self).__init__(*args, **kwargs)
        self._http_server: HttpDaemon = http_server
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._notifyBox = notify.ToolkitNotify(self.ui.textLog_2)
        self.ui.HomeDeviceConnStatusWidget.setProperty('class', 'bgLight')
        self.ui.OrderTable.setProperty('class', 'bgLight')
        self.ui.ToolsTable.setProperty('class', 'bgLight')
        self.ui.ResultTable.setProperty('class', 'bgLight')
        self.ui.timeLabel.setProperty('class', 'bgLight')
        self.ui.load_order_btn.setProperty('class', 'primaryButton')
        self.ui.submit_btn.setProperty('class', 'primaryButton')
        self.ui.DeviceConnectButton.setProperty('class', 'primaryButton')
        self.ui.DeviceDisconnectButton.setProperty('class', 'primaryButton')
        self._compare_file = None

        self._input_group = InputGroup.InputGroup({
            'orderCode': self.ui.OrderCodeEdit,
            'targetTorque': self.ui.TargetTorqueEdit,
            'firstCheckCard': self.ui.FirstCheckCardEdit,
            'recheckCard': self.ui.RecheckCardEdit,
            'recheckName': self.ui.RecheckNameEdit,
            'inspectionCode': self.ui.InspectionCodeEdit,
            'productCode': self.ui.ProductCodeEdit,
            'RFIDEdit': self.ui.RFIDEdit,
            'classificationCode': self.ui.ClassificationCodeEdit,
            'name': self.ui.NameEdit,
            'specs': self.ui.SpecsEdit,
        })

        self._config_input_group = InputGroup.InputGroup({
            'orderUrl': self.ui.OrderUrlEdit,
            'momUrl': self.ui.MOMUrlEdit,
            'deviceIP': self.ui.DeviceIPEdit,
            'devicePort': self.ui.DevicePortEdit,
        })

        self._HomeDeviceConnStatusIndicator = StatusIndicator.StatusIndicator(
            self.ui.HomeDeviceConnStatusButton,
            'DeviceConnStatus',
            success_text='已连接',
            fail_test='未连接',
            disabled=True
        )
        self._DeviceConnStatusIndicator = StatusIndicator.StatusIndicator(
            self.ui.DeviceConnStatusButton,
            'DeviceConnStatus',
            success_text='已连接',
            fail_test='未连接',
            disabled=True
        )
        self._FirstCheckResultButton = StatusIndicator.StatusIndicator(
            self.ui.FirstCheckResultButton,
            'firstCheckResult'
        )
        self._RecheckResultButton = StatusIndicator.StatusIndicator(
            self.ui.RecheckResultButton,
            'recheckResult'
        )
        self._OrderTable = table.ToolkitTable(self.ui.OrderTable)
        self._ToolsTable = table.ToolkitTable(self.ui.ToolsTable)
        self._ResultTable = table.ToolkitTable(self.ui.ResultTable)

    @property
    def order_table(self):
        return self._OrderTable

    @property
    def tools_table(self):
        return self._ToolsTable

    @property
    def result_table(self):
        return self._ResultTable

    @property
    def input_group(self):
        return self._input_group

    @property
    def config_input_group(self):
        return self._config_input_group

    @property
    def FirstCheckResultButton(self):
        return self._FirstCheckResultButton

    @property
    def RecheckResultButton(self):
        return self._RecheckResultButton

    @property
    def DeviceConnStatusIndicator(self):
        return self._DeviceConnStatusIndicator

    @property
    def HomeDeviceConnStatusIndicator(self):
        return self._HomeDeviceConnStatusIndicator

    @property
    def notify_box(self):
        return self._notifyBox
