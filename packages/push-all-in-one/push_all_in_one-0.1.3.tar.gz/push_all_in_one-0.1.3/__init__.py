"""
Push All In One - 多合一推送服务

支持多种推送方式，包括：
- 钉钉机器人
- 企业微信机器人
- 企业微信应用
- Telegram
- Discord
- 邮件推送
- Server酱
- pushplus
- 飞书
等多种推送方式
"""

__version__ = "0.1.0"

from .interfaces import Send, SendResponse
from .push import (
    CustomEmail,
    Dingtalk, 
    Discord, 
    Feishu, 
    IGot, 
    Ntfy, 
    OneBot, 
    PushDeer, 
    PushPlus, 
    Qmsg, 
    ServerChanTurbo, 
    ServerChanV3, 
    Telegram, 
    WechatApp, 
    WechatRobot, 
    XiZhi, 
    WxPusher
)
from .one import PushAllInOne, runPushAllInOne, PushType

__all__ = [
    'Send',
    'SendResponse',
    'CustomEmail',
    'Dingtalk',
    'Discord',
    'Feishu',
    'IGot',
    'Ntfy',
    'OneBot',
    'PushDeer',
    'PushPlus',
    'Qmsg',
    'ServerChanTurbo',
    'ServerChanV3',
    'Telegram',
    'WechatApp',
    'WechatRobot',
    'XiZhi',
    'WxPusher',
    'PushAllInOne',
    'runPushAllInOne',
    'PushType',
] 