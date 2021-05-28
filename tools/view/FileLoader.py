from PyQt5.QtWidgets import QFileDialog


class FileLoader:
    def __init__(self, window):
        self.window = window

    def open_file(self, title: str = "打开文件", file_types: str = "All Files (*)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self.window,
            title,
            "",
            file_types,
            options=options,
        )
        return file_name
