import logging
import json
from typing import Dict, Optional, Any, Union, TypedDict, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:telegram")

class From(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    username: str

class Chat(TypedDict):
    id: int
    first_name: str
    last_name: str
    username: str
    type: str

class Result(TypedDict):
    message_id: int
    from_: From
    chat: Chat
    date: int
    text: str

class TelegramResponse(TypedDict):
    ok: bool
    result: Result

class TelegramOption(TypedDict, total=False):
    """
    参考 https://core.telegram.org/bots/api#sendmessage
    """
    disable_notification: bool  # 静默发送，静默地发送消息。消息发布后用户会收到无声通知。
    protect_content: bool  # 阻止转发/保存，如果启用，Telegram 中的机器人消息将受到保护，不会被转发和保存。
    message_thread_id: str  # 话题 ID，可选的唯一标识符，用以向该标识符对应的话题发送消息，仅限启用了话题功能的超级群组可用

telegramOptionSchema = {
    "disable_notification": {
        "type": "boolean",
        "title": "静默发送",
        "description": "静默地发送消息。消息发布后用户会收到无声通知。",
        "required": False,
    },
    "protect_content": {
        "type": "boolean",
        "title": "阻止转发/保存",
        "description": "如果启用，Telegram 中的机器人消息将受到保护，不会被转发和保存。",
        "required": False,
    },
    "message_thread_id": {
        "type": "string",
        "title": "话题 ID",
        "description": "可选的唯一标识符，用以向该标识符对应的话题发送消息，仅限启用了话题功能的超级群组可用",
        "required": False,
    },
}

class TelegramConfig(TypedDict):
    """Telegram配置"""
    TELEGRAM_BOT_TOKEN: str  # 机器人令牌，您可以从 https://t.me/BotFather 获取 Token。
    TELEGRAM_CHAT_ID: int  # 支持对话/群组/频道的 Chat ID，您可以转发消息到 https://t.me/JsonDumpBot 获取 Chat ID
    PROXY_URL: Optional[str]  # 代理地址

telegramConfigSchema = {
    "TELEGRAM_BOT_TOKEN": {
        "type": "string",
        "title": "机器人令牌",
        "description": "您可以从 https://t.me/BotFather 获取 Token。",
        "required": True,
    },
    "TELEGRAM_CHAT_ID": {
        "type": "number",
        "title": "支持对话/群组/频道的 Chat ID",
        "description": "您可以转发消息到 https://t.me/JsonDumpBot 获取 Chat ID",
        "required": True,
    },
    "PROXY_URL": {
        "type": "string",
        "title": "代理地址",
        "description": "代理地址",
        "required": False,
    },
}

class Telegram(Send):
    """
    Telegram Bot 推送。
    官方文档：https://core.telegram.org/bots/api#making-requests
    """
    
    namespace = "Telegram"
    configSchema = telegramConfigSchema
    optionSchema = telegramOptionSchema
    
    def __init__(self, config: TelegramConfig):
        """
        初始化Telegram推送
        
        Args:
            config: Telegram配置
        """
        logger.debug(f"config: {config}")
        self.TELEGRAM_BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
        self.TELEGRAM_CHAT_ID = config["TELEGRAM_CHAT_ID"]
        self.proxyUrl = config.get("PROXY_URL")
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[TelegramOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息正文，和 title 相加后不超过 4096 个字符
            option: 其他参数
            
        Returns:
            发送结果
        """
        url = f"https://api.telegram.org/bot{self.TELEGRAM_BOT_TOKEN}/sendMessage"
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        text = f"{title}"
        if desp:
            text += f"\n{desp}"
            
        data = {
            "chat_id": self.TELEGRAM_CHAT_ID,
            "text": text,
        }
        
        if option:
            data.update(option)
            
        return await ajax(
            url=url,
            method="POST",
            proxy_url=self.proxyUrl,
            data=data,
        ) 