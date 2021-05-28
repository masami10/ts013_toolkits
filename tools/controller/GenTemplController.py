from typing import Dict, List
from tools.model.local_tmpl import G_LOCAL_TMPL, clean_dirty_data, get_local_templates, get_local_tmpls_curve_param_entry, update_local_templates
from tools.view.FileWriter import FileWriter
from tools.controller.MixinController import MixinController
from loguru import logger
from tools.model.GenTmplModel import GenTmplModel
from tools.view.FileLoader import FileLoader
import json
import copy

class GenTemplController(MixinController):
    def __init__(self, window):
        super(GenTemplController, self).__init__(window)
        self._template_compare_model = GenTmplModel()
        self.reset_button_handler()

    def reset_button_handler(self):
        self.window.ui.submit_btn.clicked.connect(self.save_param_btn)

    def params_data_changed(self, data: List[Dict]):
        if len(data) != 2:
            return
        d: Dict = get_local_tmpls_curve_param_entry(self._bolt_number)
        val = {data[0].get('value'): data[1].get('value')}
        d.update(val)

    def save_param_btn(self):
        if not self._bolt_number:
            return
        logger.info('保存修改的模板参数 螺栓编号: {}'.format(self._bolt_number))
        file_name = FileWriter(self.window).save_file(
            "保存螺栓{}模板".format(self._bolt_number), "JSON Files (*.json)")
        # data = {self._bolt_number: {}}
        clean_dirty_data()
        tt = get_local_templates()
        if not tt:
            return
        dd = copy.deepcopy(tt)
        for key in dd.keys():
            d: Dict = dd.get(key, {}).get('curve_param')
            for k in d.keys():
                d[k] = float(d.get(k))
        with open(file_name, "w") as f:
            vv = json.dumps(dd, indent=4, sort_keys=True)
            f.write(vv)
        return

    @property
    def param_table(self):
        return self.window.gen_tmpl_tab_params_table

    @property
    def item_talbe(self):
        return self.window.gen_tmpl_items_table

    def gen_bolt_tmpl(self):
        logger.info('生成曲线模板')
        #TODO: 加载加载模板曲线逻辑

    def do_action_click(self, *args, **kargs):
        super(GenTemplController, self).do_action_click(*args, **kargs)
        bolt_number = args[0]
        try:
            file_name = FileLoader(self.window).open_file(
                "加载{}曲线".format(bolt_number),
                "All Files (*);;CSV Files (*.csv);;Excel Files (*.xlst)")
            logger.info("加载曲线文件: {}, 螺栓编号: {}".format(file_name, bolt_number))
            self.set_viewing_template(bolt_number)
            self.gen_bolt_tmpl()
        except Exception as e:
            self.window.notify_box.error(repr(e))
