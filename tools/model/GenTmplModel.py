# -*- coding: utf-8 -*-
import json
from loguru import logger
from tools.model.online_tmpl import get_online_templates
from tools.model.local_tmpl import get_local_templates
from tools.model.TemplateCompareModel import TemplateCompareModel


class GenTmplModel(TemplateCompareModel):
    pass