# -*- coding: utf-8 -*-
import os
from loguru import logger
from typing import Optional
import json

G_VAR_TMPL: Optional[dict] = None


def read_online_tmpl(file_name: str) -> bool:
    global G_VAR_TMPL
    try:
        if not file_name:
            raise Exception('未指定模板文件！')
        if not os.path.isfile(file_name):
            raise Exception("打开模板文件必须是一个文件！")
        with open(file_name) as f:
            G_VAR_TMPL = json.load(f)
        return True
    except Exception as e:
        logger.error(e)
        return False


def get_online_templates():
    return G_VAR_TMPL
