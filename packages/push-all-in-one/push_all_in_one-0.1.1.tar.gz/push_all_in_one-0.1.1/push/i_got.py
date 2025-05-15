import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:i-got")

class IGotConfig(TypedDict):
    """iGot配置"""
    I_GOT_KEY: str  # 微信搜索小程序"iGot"获取推送key

iGotConfigSchema = {
    "I_GOT_KEY": {
        "type": "string",
        "title": "iGot 推送key",
        "description": "iGot 推送key",
        "required": True,
        "default": "",
    },
}

class IGotOption(TypedDict, total=False):
    """iGot选项"""
    url: str  # 链接； 点开消息后会主动跳转至此地址
    automaticallyCopy: int  # 是否自动复制； 为1自动复制
    urgent: int  # 紧急消息，为1表示紧急。此消息将置顶在小程序内， 同时会在推送的消息内做一定的特殊标识
    copy: str  # 需要自动复制的文本内容
    topic: str  # 主题； 订阅链接下有效；对推送内容分类，用户可选择性订阅

iGotOptionSchema = {
    "url": {
        "type": "string",
        "title": "链接",
        "description": "链接； 点开消息后会主动跳转至此地址",
        "required": False,
        "default": "",
    },
    "automaticallyCopy": {
        "type": "number",
        "title": "是否自动复制",
        "description": "是否自动复制； 为1自动复制",
        "required": False,
        "default": 0,
    },
    "urgent": {
        "type": "number",
        "title": "紧急消息",
        "description": "紧急消息，为1表示紧急。此消息将置顶在小程序内， 同时会在推送的消息内做一定的特殊标识",
        "required": False,
        "default": 0,
    },
    "copy": {
        "type": "string",
        "title": "需要自动复制的文本内容",
        "description": "需要自动复制的文本内容",
        "required": False,
        "default": "",
    },
    "topic": {
        "type": "string",
        "title": "主题",
        "description": "主题； 订阅链接下有效；对推送内容分类，用户可选择性订阅",
        "required": False,
        "default": "",
    },
}

class IGotData(TypedDict):
    """iGot响应数据"""
    id: str  # 消息记录，后期开放其他接口用

class IGotResponse(TypedDict):
    """iGot响应"""
    ret: int  # 状态码； 0为正常
    data: IGotData  # 响应结果
    errMsg: str  # 结果描述

class IGot(Send):
    """
    iGot 推送，官方文档：http://hellyw.com
    """
    
    namespace = "iGot"
    configSchema = iGotConfigSchema
    optionSchema = iGotOptionSchema
    
    def __init__(self, config: IGotConfig):
        """
        初始化iGot推送
        
        Args:
            config: iGot配置
        """
        self.I_GOT_KEY = config["I_GOT_KEY"]
        logger.debug(f'set I_GOT_KEY: "{self.I_GOT_KEY}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[IGotOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息正文
            option: 额外选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        
        data = {
            "title": title,
            "content": desp or title,
            "automaticallyCopy": 0,  # 关闭自动复制
            **option,
        }
        
        return await ajax(
            url=f"https://push.hellyw.com/{self.I_GOT_KEY}",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            data=data,
        ) 