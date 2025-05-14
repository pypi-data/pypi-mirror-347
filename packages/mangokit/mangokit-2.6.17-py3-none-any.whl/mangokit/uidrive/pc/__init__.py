# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description: # @Time   : 2023-07-15 12:02
# @Author : 毛鹏

from typing import Optional

import uiautomation as auto

from mangokit.uidrive._base_data import BaseData
from mangokit.uidrive.pc.element import WinElement
from mangokit.uidrive.pc.input_device import WinDeviceInput


class WinDriver(WinElement, WinDeviceInput):
    def __init__(self, base_data: BaseData):
        super().__init__(base_data)

    def find_element(
            self,
            *,
            control_type: str = "Control",
            name: Optional[str] = None,
            automation_id: Optional[str] = None,
            depth: int = 2,
            parent: Optional[auto.Control] = None,
            **extra_attrs
    ) -> auto.Control:
        """
        明确参数的元素查找方法

        必需参数（至少提供以下之一）:
            name: 控件名称
            automation_id: 控件唯一标识
            extra_attrs: 其他可唯一标识的属性

        可选参数:
            control_type: 控件类型（默认"Control"）
            depth: 搜索深度（默认2）
            parent: 父控件（默认使用base_data.window的父控件）

        返回:
            auto.Control: 找到的控件对象

        示例:
            find_element(name="确定", control_type="Button")
            find_element(automation_id="txtUsername")
            find_element(ClassName="Edit", Name="用户名")
        """
        # 参数校验
        if not any([name, automation_id, extra_attrs]):
            raise ValueError("必须提供至少一个定位参数(name/automation_id/其他属性)")

        # 设置默认父控件
        parent = parent or self.base_data.window.GetParentControl()

        # 构造搜索参数
        search_params = {
            "searchDepth": depth,
            "Timeout": 10 * 1000,
            **{
                key.capitalize() if key != "className" else "ClassName": value
                for key, value in {
                    "name": name,
                    "automationId": automation_id,
                    **extra_attrs
                }.items()
                if value is not None
            }
        }

        # 获取控件类并查找
        control_class = getattr(auto, f"{control_type}Control", auto.Control)
        control = control_class(parent=parent, **search_params)

        if not control.Exists():
            raise ElementNotFoundError(
                f"未找到控件: type={control_type}, params={search_params}"
            )
        return control


class ElementNotFoundError(Exception):
    pass
