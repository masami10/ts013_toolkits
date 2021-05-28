# -*- coding: utf-8 -*-

from typing import ItemsView
from functools import partial

from tools.model.curve_renderer import get_series_by_type, set_curves
from tools.model.AnalysisBoltsModel import AnalysisBoltsModel
from tools.model.TemplateCompareModel import TemplateCompareModel
from tools.model.GenTmplModel import GenTmplModel

from tools.view.window import ToolKitWindow
from tools.view.FileLoader import FileLoader
from tools.model import online_tmpl, local_tmpl
from loguru import logger
from typing import Optional
from PyQt5.QtWidgets import QPushButton, QTableWidget, QHeaderView, QTableWidgetItem, QToolButton, QWidget


class MixinController:
    def __init__(self, window: ToolKitWindow):
        self.window: ToolKitWindow = window
        self._template_compare_model = TemplateCompareModel()
        self._analysis_bolts_model = AnalysisBoltsModel()
        self._bolt_number: Optional[str] = None  # 当前激活的螺栓编号

    @property
    def param_table(self):
        return self.window.comapre_tab_params_table

    @property
    def item_talbe(self):
        return self.window.compare_items_table

    def do_action_click(self, *args, **kargs):
        logger.info('click')
