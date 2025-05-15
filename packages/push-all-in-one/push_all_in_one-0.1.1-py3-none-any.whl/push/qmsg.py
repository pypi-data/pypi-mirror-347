import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:qmsg")

# 推送类型，见 [Qmsg](https://qmsg.zendee.cn/docs/api)
QmsgPushType = Literal['send', 'group']

class QmsgConfig(TypedDict):
    """Qmsg酱配置"""
    QMSG_KEY: str  # 推送的 key。在 [Qmsg 酱管理台](https://qmsg.zendee.cn/user) 查看

qmsgConfigSchema = {
    "QMSG_KEY": {
        "type": "string",
        "title": "推送的 key",
        "description": "在 [Qmsg 酱管理台](https://qmsg.zendee.cn/user) 查看",
        "required": True,
    },
}

class QmsgPrivateMsgOption(TypedDict, total=False):
    """Qmsg酱私聊消息选项"""
    type: Literal['send']  # send 表示发送消息给指定的QQ号，group 表示发送消息给指定的QQ群。默认为 send
    qq: str  # 指定要接收消息的QQ号或者QQ群。多个以英文逗号分割，例如：12345,12346
    bot: Optional[str]  # 机器人的QQ号。指定使用哪个机器人来发送消息，不指定则会自动随机选择一个在线的机器人发送消息。该参数仅私有云有效

class QmsgGroupMsgOption(TypedDict, total=False):
    """Qmsg酱群聊消息选项"""
    type: Literal['group']  # send 表示发送消息给指定的QQ号，group 表示发送消息给指定的QQ群。默认为 send
    qq: str  # 指定要接收消息的QQ号或者QQ群。多个以英文逗号分割，例如：12345,12346
    bot: Optional[str]  # 机器人的QQ号。指定使用哪个机器人来发送消息，不指定则会自动随机选择一个在线的机器人发送消息。该参数仅私有云有效

# Qmsg酱选项可以是私聊或群聊
QmsgOption = Union[QmsgPrivateMsgOption, QmsgGroupMsgOption]

qmsgOptionSchema = {
    "type": {
        "type": "select",
        "title": "消息类型",
        "description": "send 表示发送消息给指定的QQ号，group 表示发送消息给指定的QQ群。默认为 send",
        "required": True,
        "default": "send",
        "options": [
            {
                "label": "私聊",
                "value": "send",
            },
            {
                "label": "群聊",
                "value": "group",
            },
        ],
    },
    "qq": {
        "type": "string",
        "title": "指定要接收消息的QQ号或者QQ群",
        "description": "多个以英文逗号分割，例如：12345,12346",
        "required": True,
    },
    "bot": {
        "type": "string",
        "title": "机器人的QQ号",
        "description": "指定使用哪个机器人来发送消息，不指定则会自动随机选择一个在线的机器人发送消息。该参数仅私有云有效",
        "required": False,
    },
}

class QmsgResponse(TypedDict):
    """Qmsg酱响应"""
    success: bool  # 本次请求是否成功
    reason: str  # 本次请求结果描述
    code: int  # 错误代码。错误代码目前不可靠，如果要判断是否成功请使用success
    info: Any  # 额外信息

class Qmsg(Send):
    """
    Qmsg酱。使用说明见 [Qmsg酱](https://qmsg.zendee.cn/docs)
    """
    
    namespace = "Qmsg酱"
    configSchema = qmsgConfigSchema
    optionSchema = qmsgOptionSchema
    
    def __init__(self, config: QmsgConfig):
        """
        初始化Qmsg酱
        
        Args:
            config: Qmsg酱配置
        """
        self.QMSG_KEY = config["QMSG_KEY"]
        logger.debug(f'set QMSG_KEY: "{self.QMSG_KEY}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: str, option: QmsgOption) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息描述
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        # 由于 Qmsg 酱的 option 中带有必填项，所以需要校验
        # 根据 optionSchema 验证 option
        validate(option, self.optionSchema)
        
        qq = option.get("qq", "")
        type_ = option.get("type", "send")
        bot = option.get("bot")
        
        # 构建消息
        msg = f"{title}{f'\\n{desp}' if desp else ''}"
        
        # 构建数据
        data = {"msg": msg, "qq": qq}
        if bot:
            data["bot"] = bot
        
        return await ajax(
            url=f"https://qmsg.zendee.cn/{type_}/{self.QMSG_KEY}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
            data=data,
        ) 