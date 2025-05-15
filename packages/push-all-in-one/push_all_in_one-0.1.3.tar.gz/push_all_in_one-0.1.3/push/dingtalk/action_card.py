from typing import List, Union
from dataclasses import dataclass, field

@dataclass
class Button:
    """按钮"""
    title: str
    actionURL: str


@dataclass
class OverallJump:
    """整体跳转ActionCard类型"""
    singleTitle: str  # 单个按钮的标题
    singleURL: str  # 点击singleTitle按钮触发的URL


@dataclass
class IndependentJump:
    """独立跳转ActionCard类型"""
    btns: List[Button] = field(default_factory=list)


@dataclass
class ActionCard:
    """钉钉动作卡片消息"""
    msgtype: str = "actionCard"
    actionCard: Union[OverallJump, IndependentJump] = None
    # 以下字段是公共的
    title: str = ""
    text: str = ""
    btnOrientation: str = "0"  # 0: 按钮竖直排列, 1: 按钮横向排列 