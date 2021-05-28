# -*- coding: utf-8 -*-
import json
from tools.model.online_tmpl import get_online_templates
from tools.model.local_tmpl import get_local_templates


def format_template_key(source, bolt, mode, group):
    return '{}/{}/{}/{}'.format(source, bolt, mode, group)


class TemplateCompareModel:
    def __init__(self):
        super(TemplateCompareModel, self).__init__()
