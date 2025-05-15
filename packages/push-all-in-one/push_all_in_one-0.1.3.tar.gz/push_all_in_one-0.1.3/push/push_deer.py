import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:push-deer")

# PushDeer推送类型
PushDeerPushType = Literal['markdown', 'text', 'image']

class PushDeerConfig(TypedDict):
    """PushDeer配置"""
    PUSH_DEER_PUSH_KEY: str  # pushkey。请参考 https://github.com/easychen/pushdeer 获取
    PUSH_DEER_ENDPOINT: Optional[str]  # 使用自架版时的服务器端地址。例如 http://127.0.0.1:8800。默认为 https://api2.pushdeer.com

pushDeerConfigSchema = {
    "PUSH_DEER_PUSH_KEY": {
        "type": "string",
        "title": "pushkey",
        "description": "请参考 https://github.com/easychen/pushdeer 获取",
        "required": True,
    },
    "PUSH_DEER_ENDPOINT": {
        "type": "string",
        "title": "使用自架版时的服务器端地址",
        "description": "例如 http://127.0.0.1:8800。默认为 https://api2.pushdeer.com",
        "required": False,
        "default": "https://api2.pushdeer.com",
    },
}

class PushDeerOption(TypedDict, total=False):
    """PushDeer选项"""
    type: PushDeerPushType  # 格式。文本=text，markdown，图片=image，默认为markdown。type 为 image 时，text 中为要发送图片的URL

pushDeerOptionSchema = {
    "type": {
        "type": "select",
        "title": "格式",
        "description": "文本=text，markdown，图片=image，默认为markdown。type 为 image 时，text 中为要发送图片的URL",
        "required": False,
        "default": "markdown",
        "options": [
            {
                "label": "文本",
                "value": "text",
            },
            {
                "label": "Markdown",
                "value": "markdown",
            },
            {
                "label": "图片",
                "value": "image",
            },
        ],
    },
}

class PushDeerContent(TypedDict):
    result: List[str]

class PushDeerResponse(TypedDict):
    """PushDeer响应"""
    code: int  # 正确为0，错误为非0
    error: str  # 错误信息。无错误时无此字段
    content: PushDeerContent  # 消息内容，错误时无此字段

class PushDeer(Send):
    """
    PushDeer 推送。 官方文档 https://github.com/easychen/pushdeer
    """
    
    namespace = "PushDeer"
    configSchema = pushDeerConfigSchema
    optionSchema = pushDeerOptionSchema
    
    def __init__(self, config: PushDeerConfig):
        """
        创建 PushDeer 实例
        
        Args:
            config: PushDeer配置
        """
        self.PUSH_DEER_PUSH_KEY = config["PUSH_DEER_PUSH_KEY"]
        self.PUSH_DEER_ENDPOINT = config.get("PUSH_DEER_ENDPOINT", "https://api2.pushdeer.com")
        logger.debug(f'set PUSH_DEER_PUSH_KEY: "{self.PUSH_DEER_PUSH_KEY}", PUSH_DEER_ENDPOINT: "{self.PUSH_DEER_ENDPOINT}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        
    async def send(self, title: str, desp: str = "", option: Optional[PushDeerOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 推送消息内容
            desp: 消息内容第二部分
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        type_ = option.get("type", "markdown")
        
        return await ajax(
            base_url=self.PUSH_DEER_ENDPOINT,
            url="/message/push",
            method="POST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "text": title,
                "desp": desp,
                "pushkey": self.PUSH_DEER_PUSH_KEY,
                "type": type_,
            },
        ) 