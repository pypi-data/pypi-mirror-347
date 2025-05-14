from unittest.mock import MagicMock

import sys

from mangokit.tools import Meta

if not sys.platform.startswith('win32'):
    WindowControl = MagicMock()
    print("警告: uiautomation 仅支持 Windows，当前环境已自动跳过")
else:
    from uiautomation.uiautomation import Control
from mangokit.uidrive._base_data import BaseData


class WinElement(metaclass=Meta):
    """元素操作"""

    def __init__(self, base_data: BaseData):
        self.base_data = base_data

    def click(self, control: Control):
        """点击控件"""
        control.Click()

    def input_text(self, control: Control, text: str):
        """输入文本"""
        control.SendKeys(text)

    def get_text(self, control: Control) -> str:
        """获取控件文本"""
        return control.Name
