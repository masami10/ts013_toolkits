# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QToolButton, QWidget
from typing import Dict, List, Any, Union
from PyQt5.QtCore import Qt
from tools.view.mixin import ToolKitMixin
from loguru import logger
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui

table_headers = ["编号", "选择"]
empty_row_data = ["", ""]


class ToolkitTable(ToolKitMixin, QWidget):
    cell_edited_signal = QtCore.pyqtSignal(list, int, int)
    row_clicked_signal = QtCore.pyqtSignal(str)
    table_render_signal = QtCore.pyqtSignal(pd.DataFrame)

    error_color = QtGui.QColor('#dc3545')

    def __init__(self, instance: QTableWidget, headers: List[str] = table_headers):
        ToolKitMixin.__init__(self, instance)
        QWidget.__init__(self)
        self._headers = headers
        self._active = False
        self.table_instance.cellDoubleClicked.connect(self.set_active)
        self.table_instance.cellChanged.connect(self.on_cell_changed)
        self.table_instance.itemClicked.connect(self.on_item_clicked)
        self.table_instance.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_render_signal.connect(self.render_table)

    def set_active(self):
        self._active = True

    def set_inactive(self):
        self._active = False

    def on_cell_changed(self, row: int, col: int):
        if not self.active:
            return
        logger.debug("行: {} , 列: {} 数据发生变化".format(row, col))
        data = self.get_row_data(row)
        self.cell_edited_signal.emit(data, row, col)
        self.set_inactive()

    def on_item_clicked(self, item):
        row = item.row()
        row_header = self.get_row_header(row)
        self.row_clicked_signal.emit(row_header)

    @property
    def active(self):
        return self._active

    @property
    def table_instance(self) -> QTableWidget:
        return self.qt_instance

    def get_row_header(self, row: int) -> str:
        t = self.table_instance
        data = t.item(row, 0).text()
        return data

    def get_row_data(self, row: int) -> List:
        t = self.table_instance
        cols = t.columnCount() + 1
        ret = []
        for i in range(cols):
            cell = t.item(row, i)
            if not cell:
                continue
            ret.append({
                'row': row,
                'col': i,
                'value': cell.text()
            })
        return ret

    def add_new_row(self):
        t = self.table_instance
        if not t:
            return
        row = t.rowCount() + 1
        t.setRowCount(row)
        self.set_table_row_item(row, empty_row_data)

    def reset_table(self, data: List[List[Any]] = None):
        tTable = self.table_instance
        tTable.clearContents()
        if not data:
            return
        ll = len(data)
        tTable.setRowCount(ll)
        for row, dd in enumerate(data):
            self.set_table_row_item(row, dd)

    def del_last_row(self):
        t = self.table_instance
        if not t:
            return
        row = t.rowCount() - 1
        t.setRowCount(row)

    def set_table_item(self, row: int, col: int, content: Union[str, QPushButton]):
        tTable = self.table_instance
        ss = content
        if not tTable:
            logger.error("Table Is Not Defined!!!")
            return
        if isinstance(content, int) or isinstance(content, float):
            ss = str(content)
        if isinstance(content, QWidget):
            tTable.setCellWidget(row, col, content)
            return
        item = QTableWidgetItem(ss)
        item.setTextAlignment(Qt.AlignCenter)
        tTable.setItem(row, col, item)

    def get_table_item(self, row: int, col: int) -> QTableWidgetItem:
        tTable = self.table_instance
        return tTable.item(row, col)

    def set_table_row_item(self, row, contents: List[str]):
        # if len(contents) != len(table_headers):
        #     logger.error("数据长度不一致！！！")
        tTable = self.table_instance
        if not tTable:
            logger.error("Table Is Not Defined!!!")
            return
        for col, content in enumerate(contents):
            self.set_table_item(row, col, content)

    def init_table_headers(self):
        if not self.qt_instance:
            return
        table_headers = self._headers
        table = self.qt_instance
        table.verticalHeader().setVisible(False)
        table.setColumnCount(len(table_headers))
        table.setHorizontalHeaderLabels(table_headers)
        header = table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignCenter)
        # header.setStyleSheet("background-color: gray")
        header.setSectionResizeMode(QHeaderView.Stretch)  # 均分显示
        header.setVisible(True)

    def render_table(self, table_content: pd.DataFrame):
        mark_error = list(table_content.get('mark_error', []))
        if 'mark_error' in table_content.columns:
            table_content=table_content.drop(columns=['mark_error'])
        tTable = self.table_instance
        tTable.clearContents()
        self._headers = table_content.keys()
        self.init_table_headers()
        d: np.ndarray = table_content.to_numpy()
        render_list = d.tolist()
        if not render_list:
            return
        ll = len(render_list)
        tTable.setRowCount(ll)
        for row, dd in enumerate(render_list):
            self.set_table_row_item(row, dd)
        if len(mark_error) > 0:
            for row, should_mark_error in enumerate(mark_error):
                if should_mark_error:
                    self.set_error(row)

    def set_error(self, row):
        t_table = self.table_instance
        for n in range(0, t_table.columnCount()):
            t_table.item(row, n).setBackground(self.error_color)
