from PyQt5.QtWidgets import QFileDialog


class FileWriter:
    def __init__(self, window):
        self.window = window

    def save_file(self, title: str = "保存文件", file_types: str = "All Files (*)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self.window,
            title,
            "",
            file_types,
            options=options,
        )
        return file_name
