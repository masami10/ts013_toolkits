# -*- coding:utf-8 -*-

from tools.controller.MixinController import MixinController
from loguru import logger
from tools.model.TemplateCompareModel import TemplateCompareModel
from tools.model.AnalysisBoltsModel import AnalysisBoltsModel
from tools.model.curve_renderer import set_curves, get_series_by_type
from tools.view.FileLoader import FileLoader
from tools.model import online_tmpl, local_tmpl


class TemplateCompareController(MixinController):

    def load_bolt_list(self):
        try:
            file_name = FileLoader(self.window).open_file(
                "打开编号文件",
                "All Files (*);;CSV Files (*.csv);;Excel Files (*.xlst)"
            )
            logger.info("打开编号文件: {}".format(file_name))
            bolts = self._analysis_bolts_model.read_analysis_bolts(file_name)
            self._template_compare_model.set_compare_bolts(bolts)
            self.update_table_content()
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def load_local_template(self):
        try:
            super(TemplateCompareController, self).load_local_template()
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def load_online_template(self):
        try:
            super(TemplateCompareController, self).load_online_template()
        except Exception as e:
            self.window.notify_box.error(repr(e))

    def do_compare(self):
        try:
            window = self.window
            window.notify_box.info("开始比对模板")
            self._template_compare_model.compare_templates()
            self.update_table_content()
            window.notify_box.info("模板比对已完成")
        except Exception as e:
            self.window.notify_box.error(repr(e))

    # def set_viewing_template(self, bolt):
    #     try:
    #         param_table = self.param_table
    #         curves_view = self.window.webViews
    #         logger.info(bolt)
    #         params = self._template_compare_model.get_curve_params(bolt)
    #         param_table.render(params)
    #         curves = self._template_compare_model.get_curves(bolt)
    #         set_curves(curves)
    #         for curve_type, curve_view in curves_view.items():
    #             series = get_series_by_type(curve_type)
    #             curve_view.set_series(series)
    #             curve_view.show_compare_diff_view()
    #     except Exception as e:
    #         self.window.notify_box.error(repr(e))
