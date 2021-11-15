# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
from ui.toolkit import Ui_MainWindow
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtCore import QTimer, QDateTime
from .mixin import ToolKitMixin
from transport.http_server import HttpServer
from tools.view import table, notify, InputGroup, StatusIndicator
from .ToolsAppendWindow import ToolsAppendWindow


class ToolKitWindow(ToolKitMixin, QtWidgets.QWidget):
    resized = QtCore.pyqtSignal()

    closeSignal = QtCore.pyqtSignal()

    def showMaximized(self) -> None:
        self.qt_instance.showMaximized()
        if self.timer:
            self.timer.start(1000)  # 定时器为1秒
        if self._http_server:
            self._http_server.start()

    def closeEvent(self, event):
        self.closeSignal.emit()
        if self.timer:
            self.timer.stop()
        if self._http_server:
            self._http_server.stop()

    def __init__(self, http_server: HttpServer, *args, **kwargs):
        main_window = QtWidgets.QMainWindow(*args, **kwargs)
        ToolKitMixin.__init__(self, main_window)
        QtWidgets.QWidget.__init__(self)
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self.qt_instance)
        self.ui.OrderTable.verticalScrollBar().setStyleSheet(
            "QScrollBar:vertical{"
            "width:40px;}"
        )
        self.tools_append_window = ToolsAppendWindow()
        # main_window.resize(1920, 1080)  # 重新设定为1920 * 1080
        self._http_server: HttpServer = http_server
        self._notifyBox = notify.ToolkitNotify([self.ui.textLog_2, self.ui.textBrowser])
        self.ui.HomeDeviceConnStatusWidget.setProperty('class', 'bgLight')
        self.ui.ToolsConfigTable.setProperty('class', 'bgLight')
        self.ui.OrderTable.setProperty('class', 'bgLight')
        self.ui.ToolsTable.setProperty('class', 'bgLight')
        self.ui.ToolsTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.ResultTable.setProperty('class', 'bgLight')
        self.ui.timeLabel.setProperty('class', 'bgLight')
        self.ui.load_server_order_btn.setProperty('class', 'primaryButton')
        self.ui.submit_btn.setProperty('class', 'primaryButton')
        self.ui.DeviceConnectButton.setProperty('class', 'primaryButton')
        self.ui.DeviceDisconnectButton.setProperty('class', 'primaryButton')
        self.ui.ToolsConfigAddButton.setProperty('class', 'primaryButton')
        self.ui.QueryOrderButton.setProperty('class', 'primaryButton')
        self.ui.CancelQueryButton.setProperty('class', 'danger')
        self.ui.ClearResultsButton.setProperty('class', 'danger')

        self.timer = QTimer()
        # 定时器结束，触发showTime方法
        self.timer.timeout.connect(self.showTime)

        self._input_group = InputGroup.InputGroup({
            'orderCode': self.ui.OrderCodeEdit,
            'targetTorque': self.ui.TargetTorqueEdit,
            'minTorque': self.ui.minTorqueEdit,
            'maxTorque': self.ui.MaxTorqueEdit,
            'firstCheckCard': self.ui.FirstCheckCardEdit,
            'recheckCard': self.ui.RecheckCardEdit,
            'FirstCheckName': self.ui.FirstCheckNameEdit,
            'recheckName': self.ui.RecheckNameEdit,
            'toolFixedInspectionCode': self.ui.InspectionCodeEdit,
            'toolMaterialCode': self.ui.ProductCodeEdit,
            'toolRfid': self.ui.RFIDEdit,
            'toolClassificationCode': self.ui.ClassificationCodeEdit,
            'toolName': self.ui.NameEdit,
            'toolSpecificationType': self.ui.SpecsEdit,
        })

        self._config_input_group = InputGroup.InputGroup({
            'orderUrl': self.ui.OrderUrlEdit,
            'momUrl': self.ui.MOMUrlEdit,
            'operationUrl': self.ui.OperationUrlEdit,
            'workCenter': self.ui.workCenterLabelEdit,
        })
        self._device_config_group = InputGroup.InputGroup({
            'ip': self.ui.DeviceIPEdit,
            'port': self.ui.DevicePortEdit,
        })

        self._person_config_group = InputGroup.InputGroup({
            'originPersonCode': self.ui.FirstCheckCardEdit,
            'originPersonName': self.ui.FirstCheckNameEdit,
            'recheckPersonCode': self.ui.RecheckCardEdit,
            'recheckPersonName': self.ui.RecheckNameEdit,
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
        self._OrderTable = table.ToolkitTable(self.ui.OrderTable)
        self._ToolsTable = table.ToolkitTable(self.ui.ToolsTable)
        self._ResultTable = table.ToolkitTable(self.ui.ResultTable)
        self._ToolsConfigTable = table.ToolkitTable(self.ui.ToolsConfigTable)

    def showTime(self):
        # 获取系统当前时间
        time = QDateTime.currentDateTime()
        # 设置系统时间的显示格式
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        # 在标签上显示时间
        self.ui.timeLabel.setText(timeDisplay)

    @property
    def order_table(self):
        return self._OrderTable

    @property
    def tools_table(self):
        return self._ToolsTable

    @property
    def tools_config_table(self):
        return self._ToolsConfigTable

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
    def device_config_group(self):
        return self._device_config_group

    @property
    def person_config_group(self):
        return self._person_config_group


    @property
    def DeviceConnStatusIndicator(self):
        return self._DeviceConnStatusIndicator

    @property
    def HomeDeviceConnStatusIndicator(self):
        return self._HomeDeviceConnStatusIndicator

    @property
    def notify_box(self):
        return self._notifyBox
