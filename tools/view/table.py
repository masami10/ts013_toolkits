# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QToolButton, QWidget
from typing import Dict, List, Any, Union
from PyQt5.QtCore import Qt
from tools.view.mixin import ToolKitMixin
from loguru import logger

table_headers = ["编号", "对比结果"]
empty_row_data = ["", ""]


class ToolkitTable(ToolKitMixin):

    def __init__(self, instance: QTableWidget, headers: List[str] = table_headers):
        super(ToolkitTable, self).__init__(instance)
        self._headers = headers
        self._actived= False

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
        if isinstance(content, QPushButton) or isinstance(content, QToolButton):
            tTable.setCellWidget(row, col, content)
            return
        item = QTableWidgetItem(ss)
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
        header.setStyleSheet("background-color: gray")
        header.setSectionResizeMode(QHeaderView.Stretch)  # 均分显示
        header.setVisible(True)

    def render(self, table_content):
        tTable = self.table_instance
        tTable.clearContents()
        self._headers = table_content.keys()
        self.init_table_headers()
        # if not render_list:
        #     return
        # ll = len(render_list)
        # tTable.setRowCount(ll)
        # for row, dd in enumerate(render_list):
        #     self.set_table_row_item(row, dd)
