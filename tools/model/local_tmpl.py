# -*- coding: utf-8 -*-
import os
from loguru import logger
from typing import Optional, Dict
import json

G_LOCAL_TMPL: Optional[dict] = None


def read_local_tmpl(file_name: str) -> bool:
    global G_LOCAL_TMPL
    try:
        if not file_name:
            raise Exception('未指定模板文件！')
        if not os.path.isfile(file_name):
            raise Exception("打开模板文件必须是一个文件！")
        with open(file_name) as f:
            G_LOCAL_TMPL = json.load(f)
        return True
    except Exception as e:
        logger.error(e)
        return False


def get_local_templates():
    return G_LOCAL_TMPL

def get_local_tmpls_curve_param_entry(key:str):
    global G_LOCAL_TMPL
    return G_LOCAL_TMPL.get(key, {}).get('curve_param')

def update_local_templates(data: Dict) -> Dict:
    global G_LOCAL_TMPL
    if not G_LOCAL_TMPL:
        logger.error("请先加载本地模板!!!")
        return None
    G_LOCAL_TMPL.update(data)
    return G_LOCAL_TMPL


def clean_dirty_data() -> Dict:
    global G_LOCAL_TMPL
    for key, val in G_LOCAL_TMPL.items():
        d = G_LOCAL_TMPL.get(key)
        if isinstance(d, Dict) and d.get('0'):
            del d['0']

