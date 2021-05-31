# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore  # import PyQt5 widgets
from ui.toolkit import Ui_MainWindow
from loguru import logger
from typing import Dict, List, Any
from transport.http_server import HttpDaemon
from tools.view import table, notify, InputGroup

demo_table_items = [["006R_1_1_1", "2", "3"], ["006R_1_1_2", "22", "342"]]


class ToolKitWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    template_bolt_selected_signal = QtCore.pyqtSignal(str)
    gen_tmpl_bolt_selected_signal = QtCore.pyqtSignal(str)
    gen_tmpl_params_data_changed_signal = QtCore.pyqtSignal(list)

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
        # self._gen_tmpl_items_table = table.ToolkitTable(self.ui.tableWidget_2)
        # self._params_table = table.ToolkitTable(self.ui.tableParams_2)
        self._notifyBox = notify.ToolkitNotify(self.ui.textLog_2)
        # self.set_mock_table_data()
        self.ui.tableWidget.setProperty('class', 'bgLight')
        self.ui.tableWidget_2.setProperty('class', 'bgLight')
        self.ui.tableWidget_3.setProperty('class', 'bgLight')
        self.ui.timeLabel.setProperty('class', 'bgLight')
        self.ui.OrderCodeLabel.setProperty('class', 'height20')
        self.ui.load_order_btn.setProperty('class', 'primaryButton')
        self.ui.submit_btn.setProperty('class', 'primaryButton')
        self.ui.FirstCheckResultButton.setProperty('class', 'success resultButton resultButtonSuccess')
        self.ui.RecheckResultButton.setProperty('class',
                                                'success resultButton resultButtonSuccess')  # danger resultButton resultButtonFailed
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
        self.reset_button_handler()

    @property
    def input_group(self):
        return self._input_group

    def reset_button_handler(self):
        pass
        # self.ui.add_row_2.clicked.connect(self.add_new_row)
        # self.ui.del_row_2.clicked.connect(self.del_last_row)
        # self.gen_tmpl_items_table.table_instance.itemClicked.connect(
        #     self.on_gen_tmpl_item_table_row_clicked)

    @staticmethod
    def get_table_item_data(table: table.ToolkitTable,
                            item: QtWidgets.QTableWidgetItem) -> str:
        row = item.row()
        data = table.get_row_header(row)
        return data

    def on_gen_tmpl_params_table_cell_actived(self, row, col):
        self.gen_tmpl_tab_params_table._actived = True

    def on_gen_tmpl_params_table_cell_changed(self, row: int, col: int):
        if not self.gen_tmpl_tab_params_table._actived:
            return
        data = self.gen_tmpl_tab_params_table.get_row_data(row)
        logger.debug("行: {} , 列: {} 数据发生变化".format(row, col))
        self.gen_tmpl_params_data_changed_signal.emit(data)

    def on_compare_item_table_row_clicked(self,
                                          item: QtWidgets.QTableWidgetItem):
        bolt = self.get_table_item_data(self.compare_items_table, item)
        self.template_bolt_selected_signal.emit(bolt)

    def on_gen_tmpl_item_table_row_clicked(self,
                                           item: QtWidgets.QTableWidgetItem):
        bolt = self.get_table_item_data(self.gen_tmpl_items_table, item)
        self.gen_tmpl_bolt_selected_signal.emit(bolt)

    @property
    def compare_items_table(self):
        return self._compare_bolt_table

    @property
    def gen_tmpl_items_table(self):
        return self._gen_tmpl_items_table

    @property
    def comapre_tab_params_table(self):
        return self._params_table

    @property
    def gen_tmpl_tab_params_table(self):
        return self._gen_tmpl_params_table

    @property
    def notify_box(self):
        return self._notifyBox

    def add_new_row(self):
        if not self.compare_items_table:
            return
        t = self.compare_items_table
        t.add_new_row()

    def del_last_row(self):
        if not self.compare_items_table:
            return
        t = self.compare_items_table
        t.del_last_row()

    def reset_compare_bolt_table(self, data: List[Any] = None):
        tTable = self.compare_items_table
        if not tTable:
            logger.error("Table Is Not Defined!!!")
            return
        tTable.reset_table(data)

    def set_mock_table_data(self):
        self.reset_compare_bolt_table(demo_table_items)
        tTable = self.compare_items_table
        for row, data in enumerate(demo_table_items):
            tTable.set_table_row_item(row, data)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ToolKitWindow, self).resizeEvent(event)
