import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:server-chan-turbo")

# Server酱通道值
ChannelValue = Literal['98', '66', '1', '2', '3', '8', '0', '88', '18', '9']

# 通道支持多个，用|分隔
Channel = str  # 如 "98" 或 "98|66"

class ServerChanTurboConfig(TypedDict):
    """Server酱 Turbo 配置"""
    SERVER_CHAN_TURBO_SENDKEY: str  # Server酱 Turbo 的 SCTKEY，请前往 https://sct.ftqq.com/sendkey 领取

serverChanTurboConfigSchema = {
    "SERVER_CHAN_TURBO_SENDKEY": {
        "type": "string",
        "title": "SCTKEY",
        "description": "Server酱 Turbo 的 SCTKEY。请前往 https://sct.ftqq.com/sendkey 领取",
        "required": True,
    },
}

class ServerChanTurboOption(TypedDict, total=False):
    """Server酱 Turbo 选项"""
    short: str  # 消息卡片内容，选填。最大长度 64。如果不指定，将自动从 desp 中截取生成。
    noip: Union[str, int, bool]  # 是否隐藏调用 IP，选填。如果不指定，则显示；为 1/true 则隐藏。
    channel: Channel  # 动态指定本次推送使用的消息通道，选填。如不指定，则使用网站上的消息通道页面设置的通道。支持最多两个通道，多个通道值用竖线 "|" 隔开。
    openid: str  # 消息抄送的 openid，选填。只支持测试号和企业微信应用消息通道。多个 openid 用 "," 隔开。企业微信应用消息通道的 openid 参数，内容为接收人在企业微信中的 UID，多个人请 "|" 隔开。

serverChanTurboOptionSchema = {
    "short": {
        "type": "string",
        "title": "消息卡片内容",
        "description": "选填。最大长度 64。如果不指定，将自动从 desp 中截取生成。",
        "required": False,
    },
    "noip": {
        "type": "boolean",
        "title": "是否隐藏调用 IP",
        "description": "选填。如果不指定，则显示；为 1/true 则隐藏。",
        "required": False,
    },
    "channel": {
        "type": "string",
        "title": "消息通道",
        "description": "选填。动态指定本次推送使用的消息通道，支持最多两个通道，多个通道值用竖线 \"|\" 隔开。",
        "required": False,
    },
    "openid": {
        "type": "string",
        "title": "消息抄送的 openid",
        "description": "选填。只支持测试号和企业微信应用消息通道。多个 openid 用 \",\" 隔开。企业微信应用消息通道的 openid 参数，内容为接收人在企业微信中的 UID，多个人请 \"|\" 隔开。",
        "required": False,
    },
}

class ServerChanTurboData(TypedDict):
    """Server酱 Turbo 响应数据"""
    pushid: str  # 推送消息的 ID
    readkey: str  # 推送消息的阅读凭证
    error: str  # 错误信息
    errno: int  # 错误码

class ServerChanTurboResponse(TypedDict):
    """Server酱 Turbo 响应"""
    code: int  # 0 表示成功，其他值表示失败
    message: str  # 消息
    data: ServerChanTurboData  # 数据

class ServerChanTurbo(Send):
    """
    Server 酱·Turbo
    文档 https://sct.ftqq.com/
    """
    
    namespace = "Server酱·Turbo"
    configSchema = serverChanTurboConfigSchema
    optionSchema = serverChanTurboOptionSchema
    
    def __init__(self, config: ServerChanTurboConfig):
        """
        初始化 Server 酱·Turbo
        
        Args:
            config: 配置项
        """
        self.SCTKEY = config["SERVER_CHAN_TURBO_SENDKEY"]
        logger.debug(f'set SCTKEY: "{self.SCTKEY}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: str = "", option: Optional[ServerChanTurboOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息的标题
            desp: 消息的内容，支持 Markdown
            option: 额外发送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        
        # 处理noip参数
        if option.get("noip") in (1, True):
            option["noip"] = "1"
        
        # 构建数据
        data = {
            "text": title,
            "desp": desp,
            **option,
        }
        
        return await ajax(
            url=f"https://sctapi.ftqq.com/{self.SCTKEY}.send",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=data,
        ) 