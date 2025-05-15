import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate
from ..utils.helper import warn

logger = logging.getLogger("push:one-bot")

# OneBot消息类型
OneBotMsgType = Literal['private', 'group']

class OneBotConfig(TypedDict):
    """OneBot配置"""
    ONE_BOT_BASE_URL: str  # OneBot HTTP 基础路径
    ONE_BOT_ACCESS_TOKEN: Optional[str]  # OneBot AccessToken，出于安全原因，请务必设置 AccessToken

oneBotConfigSchema = {
    "ONE_BOT_BASE_URL": {
        "type": "string",
        "title": "OneBot HTTP 基础路径",
        "description": "OneBot HTTP 基础路径",
        "required": True,
    },
    "ONE_BOT_ACCESS_TOKEN": {
        "type": "string",
        "title": "OneBot AccessToken",
        "description": "出于安全原因，请务必设置 AccessToken",
        "required": False,
    },
}

class OneBotPrivateMsgOption(TypedDict, total=False):
    """OneBot私聊消息选项"""
    message_type: Literal['private']  # 消息类型
    user_id: int  # 对方 QQ 号
    auto_escape: bool  # 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效

class OneBotGroupMsgOption(TypedDict, total=False):
    """OneBot群聊消息选项"""
    message_type: Literal['group']  # 消息类型
    group_id: int  # 群号
    auto_escape: bool  # 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效

# OneBot选项可以是私聊或群聊
OneBotOption = Union[OneBotPrivateMsgOption, OneBotGroupMsgOption]

oneBotOptionSchema = {
    "message_type": {
        "type": "select",
        "title": "消息类型",
        "description": "消息类型，private 或 group，默认为 private",
        "required": True,
        "default": "private",
        "options": [
            {
                "label": "私聊",
                "value": "private",
            },
            {
                "label": "群聊",
                "value": "group",
            },
        ],
    },
    "user_id": {
        "type": "number",
        "title": " QQ 号",
        "description": "对方 QQ 号。仅私聊有效。",
        "required": False,
    },
    "group_id": {
        "type": "number",
        "title": "群号",
        "description": "群号。仅群聊有效。",
        "required": False,
    },
    "auto_escape": {
        "type": "boolean",
        "title": "消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效",
        "description": "消息内容是否作为纯文本发送（即不解析 CQ 码），只在 message 字段是字符串时有效",
        "required": False,
    },
}

class OneBotData(TypedDict):
    """OneBot响应数据"""
    ClassType: str  # 类型
    message_id: int  # 消息 ID

class OneBotResponse(TypedDict):
    """OneBot响应"""
    status: str  # 状态
    retcode: int  # 返回码
    data: OneBotData  # 数据
    echo: Optional[Any]  # 回声

class OneBot(Send):
    """
    OneBot。官方文档：https://github.com/botuniverse/onebot-11
    本项目实现的版本为 OneBot 11
    """
    
    namespace = "OneBot"
    configSchema = oneBotConfigSchema
    optionSchema = oneBotOptionSchema
    
    # OneBot 协议版本号
    version = 11
    
    def __init__(self, config: OneBotConfig):
        """
        创建 OneBot 实例
        
        Args:
            config: OneBot 配置
        """
        self.ONE_BOT_BASE_URL = config["ONE_BOT_BASE_URL"]
        self.ONE_BOT_ACCESS_TOKEN = config.get("ONE_BOT_ACCESS_TOKEN")
        
        logger.debug(f'set ONE_BOT_BASE_URL: "{self.ONE_BOT_BASE_URL}", ONE_BOT_ACCESS_TOKEN: "{self.ONE_BOT_ACCESS_TOKEN}"')
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        
        if not self.ONE_BOT_ACCESS_TOKEN:
            warn("未提供 ONE_BOT_ACCESS_TOKEN ！出于安全原因，请务必设置 AccessToken！")
    
    async def send(self, title: str, desp: str, option: OneBotOption) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息正文
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        # 由于 OneBot 的 option 中带有必填项，所以需要校验
        # 根据 optionSchema 验证 option
        validate(option, self.optionSchema)
        
        message_type = option.get("message_type", "private")
        
        if message_type == "private" and "user_id" not in option:
            raise Exception("OneBot 私聊消息类型必须提供 user_id")
        
        if message_type == "group" and "group_id" not in option:
            raise Exception("OneBot 群聊消息类型必须提供 group_id")
        
        # 移除已处理的选项
        option_copy = {k: v for k, v in option.items() if k != "message_type"}
        
        # 构建消息
        message = f"{title}{f'\\n{desp}' if desp else ''}"
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.ONE_BOT_ACCESS_TOKEN:
            headers["Authorization"] = f"Bearer {self.ONE_BOT_ACCESS_TOKEN}"
        
        # 构建数据
        data = {
            "auto_escape": False,
            "message_type": message_type,
            "message": message,
            **option_copy,
        }
        
        return await ajax(
            base_url=self.ONE_BOT_BASE_URL,
            url="/send_msg",
            method="POST",
            headers=headers,
            data=data,
        ) 