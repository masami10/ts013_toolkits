# -*- coding:utf-8 -*-

from .GenTemplController import GenTemplController
from PyQt5 import QtWidgets  # import PyQt5 widgets
import sys
import os
from qt_material import apply_stylesheet
from ..view import window as main_window
from .TemplateCompareController import TemplateCompareController


class AppController:

    def __init__(self):
        # Create the application object
        self.app = QtWidgets.QApplication(sys.argv)

        # Create the form object
        self.window = main_window.ToolKitWindow()
        self.init_controllers()
        self.connect_signals()
        self.apply_material_theme()

    def apply_material_theme(self):

        extra = {
            # Button colors
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#66bb6a',

            # Font
            'font-family': 'Roboto',
        }

        apply_stylesheet(self.app, theme='light_blue.xml', extra=extra)
        stylesheet = self.app.styleSheet()
        with open('styles/custom.css') as file:
            self.app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    def run_app(self):
        # Show form
        self.window.show()

        # Run the program
        sys.exit(self.app.exec())

    template_compare_controller: TemplateCompareController = None
    gen_tmpl_controller: GenTemplController = None

    def init_controllers(self):
        self.template_compare_controller = TemplateCompareController(self.window)
        self.gen_tmpl_controller = GenTemplController(self.window)

    def connect_signals(self):
        window = self.window
        ui = window.ui
        ### tab 1 曲线对比
        ui.load_order_btn.clicked.connect(self.template_compare_controller.load_bolt_list)
        ui.submit_btn.clicked.connect(self.template_compare_controller.load_online_template)
        #
        # window.template_bolt_selected_signal.connect(self.template_compare_controller.set_viewing_template)
        # window.gen_tmpl_bolt_selected_signal.connect(self.gen_tmpl_controller.set_viewing_template)
        # window.gen_tmpl_params_data_changed_signal.connect(self.gen_tmpl_controller.params_data_changed)
