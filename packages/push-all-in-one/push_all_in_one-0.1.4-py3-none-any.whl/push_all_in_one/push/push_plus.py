import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:push-plus")

# PushPlus模板类型
PushPlusTemplateType = Literal['html', 'txt', 'json', 'markdown', 'cloudMonitor', 'jenkins', 'route']

# PushPlus渠道类型
PushPlusChannelType = Literal['wechat', 'webhook', 'cp', 'sms', 'mail']

class PushPlusConfig(TypedDict):
    """PushPlus配置"""
    PUSH_PLUS_TOKEN: str  # 请前往 https://www.pushplus.plus 领取

pushPlusConfigSchema = {
    "PUSH_PLUS_TOKEN": {
        "type": "string",
        "title": "PushPlus Token",
        "description": "请前往 https://www.pushplus.plus/ 领取",
        "required": True,
    },
}

class PushPlusOption(TypedDict, total=False):
    """PushPlus选项"""
    template: PushPlusTemplateType  # 模板类型
    channel: PushPlusChannelType  # 渠道类型
    topic: str  # 群组编码，不填仅发送给自己；channel为webhook时无效
    webhook: str  # webhook编码，仅在channel使用webhook渠道和CP渠道时需要填写
    callbackUrl: str  # 发送结果回调地址
    timestamp: int  # 毫秒时间戳。格式如：1632993318000。服务器时间戳大于此时间戳，则消息不会发送

pushPlusOptionSchema = {
    "template": {
        "type": "select",
        "title": "模板类型",
        "description": "html，txt，json，markdown，cloudMonitor，jenkins，route",
        "required": False,
        "default": "html",
        "options": [
            {
                "label": "HTML",
                "value": "html",
            },
            {
                "label": "文本",
                "value": "txt",
            },
            {
                "label": "JSON",
                "value": "json",
            },
            {
                "label": "Markdown",
                "value": "markdown",
            },
            {
                "label": "阿里云监控",
                "value": "cloudMonitor",
            },
            {
                "label": "Jenkins",
                "value": "jenkins",
            },
            {
                "label": "路由器",
                "value": "route",
            },
        ],
    },
    "channel": {
        "type": "select",
        "title": "渠道类型",
        "description": "wechat，webhook，cp，sms，mail",
        "required": False,
        "default": "wechat",
        "options": [
            {
                "label": "微信",
                "value": "wechat",
            },
            {
                "label": "Webhook",
                "value": "webhook",
            },
            {
                "label": "企业微信",
                "value": "cp",
            },
            {
                "label": "邮件",
                "value": "mail",
            },
            {
                "label": "短信",
                "value": "sms",
            },
        ],
    },
    "topic": {
        "type": "string",
        "title": "群组编码",
        "description": "不填仅发送给自己；channel为webhook时无效",
        "required": False,
        "default": "",
    },
    "webhook": {
        "type": "string",
        "title": "webhook编码",
        "description": "仅在channel使用webhook渠道和CP渠道时需要填写",
        "required": False,
        "default": "",
    },
    "callbackUrl": {
        "type": "string",
        "title": "发送结果回调地址",
        "description": "发送结果回调地址",
        "required": False,
        "default": "",
    },
    "timestamp": {
        "type": "number",
        "title": "毫秒时间戳",
        "description": "格式如：1632993318000。服务器时间戳大于此时间戳，则消息不会发送",
        "required": False,
        # "default": 0,
    },
}

class PushPlusResponse(TypedDict):
    """PushPlus响应"""
    code: int  # 200 为正确
    msg: str  # 消息
    data: Any  # 数据

class PushPlus(Send):
    """
    pushplus 推送加开放平台，仅支持一对一推送。官方文档：https://www.pushplus.plus/doc/
    """
    
    namespace = "PushPlus"
    configSchema = pushPlusConfigSchema
    optionSchema = pushPlusOptionSchema
    
    def __init__(self, config: PushPlusConfig):
        """
        初始化PushPlus
        
        Args:
            config: PushPlus配置
        """
        self.PUSH_PLUS_TOKEN = config["PUSH_PLUS_TOKEN"]
        logger.debug(f'set PUSH_PLUS_TOKEN: "{self.PUSH_PLUS_TOKEN}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: str = "", option: Optional[PushPlusOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息内容
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        template = option.get("template", "html")
        channel = option.get("channel", "wechat")
        
        # 移除已处理的选项
        option_copy = {k: v for k, v in option.items() if k != "template" and k != "channel"}
        
        # 设置内容
        content = desp or title
        
        # 构建数据
        data = {
            "token": self.PUSH_PLUS_TOKEN,
            "title": title,
            "content": content,
            "template": template,
            "channel": channel,
            **option_copy,
        }
        
        return await ajax(
            url="http://www.pushplus.plus/send",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            data=data,
        ) 