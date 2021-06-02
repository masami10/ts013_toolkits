# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMainWindow

from ..view import window as main_window
from ..view.ToolsAppendWindow import ToolsAppendWindow


class ToolsAppendController:
    append_window: ToolsAppendWindow
    _content: dict

    def __init__(self, window: main_window.ToolKitWindow, on_save):
        self.window = window
        self.notify = self.window.notify_box
        self._content = {}
        self.handle_save = on_save
        self.append_window = self.window.tools_append_window
        self.connect_tools_append_window_signals()
        self.render()

    def connect_tools_append_window_signals(self):
        self.append_window.ui.SaveButton.clicked.connect(self.on_save)
        self.append_window.ui.CancelButton.clicked.connect(self.on_cancel)
        self.append_window.input_group.inputChanged.connect(self.on_edit)

    def on_edit(self, key, value):
        self._content.update({
            key: value
        })

    def on_save(self):
        self.handle_save(self._content)
        self.close_window()

    def on_cancel(self):
        self.close_window()

    def close_window(self):
        window: QMainWindow = self.append_window.qt_instance
        window.close()

    def create(self):
        self._content = {
            'toolFixedInspectionCode': '',
            'toolMaterialCode': '',
            'toolRfid': '',
            'toolClassificationCode': '',
            'toolName': '',
            'toolSpecificationType': '',
        }
        window: QMainWindow = self.append_window.qt_instance
        window.setWindowTitle('添加工具')
        window.show()
        self.render()

    def edit(self, tool: dict):
        self._content = tool
        window: QMainWindow = self.append_window.qt_instance
        window.setWindowTitle('编辑工具')
        self.append_window.qt_instance.show()
        self.render()

    def render(self):
        self.append_window.input_group.set_texts(self._content)
