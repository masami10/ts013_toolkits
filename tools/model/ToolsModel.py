import pandas as pd
from store.types import ToolsTorqueInfo
from store.store import StorageData
from py_singleton import singleton
from store.sql import query_torque_check_status
from .OrdersModel import OrdersModel
from datetime import date


def is_checked(check_date):
    today = date.today()
    if not check_date:
        return False
    if isinstance(check_date, int):
        check_date = date.fromtimestamp(check_date / 1e3)
    elif isinstance(check_date, str):
        check_date = date.fromisoformat(check_date)
    return check_date == today


def get_check_status(tool, torque):
    check_status = query_torque_check_status([(tool, torque)], )
    if check_status.empty:
        return 0
    if is_checked(check_status.at[0, 'recheck_date']):
        return 2
    if is_checked(check_status.at[0, 'first_check_date']):
        return 1
    return 0


@singleton
class ToolsModel:
    _selected_torque: ToolsTorqueInfo

    def __init__(self):
        self._store = StorageData()
        self._selected_torque = None

    @property
    def content(self) -> pd.DataFrame:
        tools = self._store.get_tools()
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
            'torque': []
        })
        for key, value in tools.items():
            tdf = tdf.append(value.to_dict, ignore_index=True)
        return tdf

    @property
    def content_current_order(self):
        tdf = pd.DataFrame({
            'toolFixedInspectionCode': [],
            'toolMaterialCode': [],
            'toolRfid': [],
            'toolClassificationCode': [],
            'toolName': [],
            'toolSpecificationType': [],
            'torque': []
        })

        if not OrdersModel().selected_orders:
            return tdf
        torques = OrdersModel().selected_order_torques

        for t in torques:
            d = t.to_dict
            check_status = get_check_status(t.toolFixedInspectionCode, t.torque)
            d.update({
                'check_status': check_status
            })
            tdf = tdf.append(pd.DataFrame(d), ignore_index=True)
        return tdf

    @property
    def selected_torque(self):
        return self._selected_torque

    def is_selected(self, tool, torque):
        if not self._selected_torque:
            return False
        return self._selected_torque.toolFixedInspectionCode == tool and self._selected_torque.torque == torque

    def set_selected_torque(self, tool_inspect_code: str, torque: str):
        torque_info = next(t for t in OrdersModel().selected_order_torques if
                           t.torque == torque and t.toolFixedInspectionCode == tool_inspect_code)
        if not torque_info:
            self._selected_torque = None
            return
        self._selected_torque = torque_info
