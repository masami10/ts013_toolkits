# -*- coding: utf-8 -*-
import os


class AnalysisBoltsModel:
    bolts = None

    def is_bolts_loaded(self):
        return self.bolts is not None and len(self.bolts['编号']) > 0

    def read_analysis_bolts(self, file_name: str):
        if not file_name:
            raise Exception('未选中编号文件！')
        if not os.path.isfile(file_name):
            raise Exception("打开编号文件必须是一个文件！")
        suffix: str = os.path.splitext(file_name)[-1]
        data = {}
        self.bolts = data
        return data
