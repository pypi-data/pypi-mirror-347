import time
import json
from typing import Dict, Any, Optional, Union, ClassVar
from dataclasses import dataclass, field, asdict

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..interfaces.schema import ConfigSchema, OptionSchema, SchemaField
from ..utils.crypto import generate_signature
from ..utils.ajax import async_request
from ..utils.helper import warn, debug
from ..utils.validate import validate
from .dingtalk import Text, Markdown, Link, ActionCard, FeedCard, IndependentJump, OverallJump

@dataclass
class DingtalkConfig:
    """钉钉机器人配置"""
    DINGTALK_ACCESS_TOKEN: str  # 钉钉机器人 access_token
    DINGTALK_SECRET: Optional[str] = None  # 加签安全秘钥(HmacSHA256)


DingtalkMsgType = str  # 'text' | 'markdown' | 'link' | 'actionCard' | 'feedCard'


class DingtalkOptionType:
    """钉钉推送选项"""
    pass


@dataclass
class DingtalkResponse:
    """钉钉响应"""
    errcode: int
    errmsg: str


class Dingtalk(Send):
    """
    钉钉机器人推送
    官方文档: https://developers.dingtalk.com/document/robots/custom-robot-access
    """
    
    namespace: ClassVar[str] = "钉钉"
    
    config_schema: ClassVar[Dict[str, SchemaField]] = {
        "DINGTALK_ACCESS_TOKEN": SchemaField(
            field_type="string",
            title="钉钉机器人 access_token",
            description="钉钉机器人 access_token",
            required=True
        ),
        "DINGTALK_SECRET": SchemaField(
            field_type="string",
            title="加签安全秘钥（HmacSHA256）",
            required=False
        )
    }
    
    option_schema: ClassVar[Dict[str, SchemaField]] = {
        "msgtype": SchemaField(
            field_type="select",
            title="消息类型",
            description="消息类型",
            required=False,
            default="text",
            options=[
                {"label": "文本", "value": "text"},
                {"label": "Markdown", "value": "markdown"},
                {"label": "链接", "value": "link"},
                {"label": "按钮", "value": "actionCard"},
                {"label": "FeedCard", "value": "feedCard"}
            ]
        )
    }
    
    def __init__(self, config: DingtalkConfig):
        self.access_token = config.DINGTALK_ACCESS_TOKEN
        self.secret = config.DINGTALK_SECRET
        self.webhook = "https://oapi.dingtalk.com/robot/send"
        self.proxy_url = None
        
        # 验证配置
        validate(vars(config), self.config_schema)
        
        debug("dingtalk", f"初始化钉钉推送, token: {self.access_token[:5]}..., secret: {self.secret and self.secret[:5]}...")
        
        if not self.secret:
            warn("未提供 DINGTALK_SECRET！")
    
    def _get_sign(self, timestamp: int) -> str:
        """获取签名"""
        if not self.secret:
            return ""
            
        sign = generate_signature(timestamp, self.secret)
        debug("dingtalk", f"生成签名: {timestamp}\\n{self.secret} -> {sign}")
        return sign
    
    async def send(self, title: str, desp: Optional[str] = None, options: Any = None) -> SendResponse:
        """
        发送钉钉消息
        
        Args:
            title: 消息标题
            desp: 消息内容，支持 Markdown
            options: 发送选项
            
        Returns:
            SendResponse: 发送响应
        """
        debug("dingtalk", f"title: {title}, desp: {desp}, options: {options}")
        
        # 默认使用text类型
        msg_type = "text"
        if options and hasattr(options, "msgtype"):
            msg_type = options.msgtype
        
        data = None
        
        if msg_type == "text":
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{title}{desp and '\\n' + desp or ''}"
                }
            }
            if options and hasattr(options, "at"):
                data["at"] = asdict(options.at)
                
        elif msg_type == "markdown":
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": title,
                    "text": f"# {title}{desp and '\\n\\n' + desp or ''}"
                }
            }
            if options and hasattr(options, "at"):
                data["at"] = asdict(options.at)
                
        elif msg_type == "link":
            if not options or not hasattr(options, "link"):
                raise ValueError("link类型消息必须提供link选项")
                
            data = {
                "msgtype": "link",
                "link": {
                    "title": title,
                    "text": desp or "",
                    "picUrl": options.link.picUrl if hasattr(options.link, "picUrl") else "",
                    "messageUrl": options.link.messageUrl if hasattr(options.link, "messageUrl") else ""
                }
            }
            
        elif msg_type == "actionCard":
            if not options or not hasattr(options, "actionCard"):
                raise ValueError("actionCard类型消息必须提供actionCard选项")
                
            data = {
                "msgtype": "actionCard",
                "actionCard": {
                    "title": title,
                    "text": desp or "",
                    "btnOrientation": options.actionCard.btnOrientation if hasattr(options.actionCard, "btnOrientation") else "0"
                }
            }
            
            if hasattr(options.actionCard, "singleTitle") and hasattr(options.actionCard, "singleURL"):
                data["actionCard"]["singleTitle"] = options.actionCard.singleTitle
                data["actionCard"]["singleURL"] = options.actionCard.singleURL
            elif hasattr(options.actionCard, "btns"):
                data["actionCard"]["btns"] = [asdict(btn) for btn in options.actionCard.btns]
                
        elif msg_type == "feedCard":
            if not options or not hasattr(options, "feedCard") or not hasattr(options.feedCard, "links"):
                raise ValueError("feedCard类型消息必须提供feedCard.links选项")
                
            data = {
                "msgtype": "feedCard",
                "feedCard": {
                    "links": [asdict(link) for link in options.feedCard.links]
                }
            }
        
        # 生成时间戳和签名
        timestamp = int(time.time() * 1000)
        sign = self._get_sign(timestamp)
        
        # 发送请求
        result = await async_request(
            url=self.webhook,
            method="POST",
            headers={"Content-Type": "application/json"},
            query={
                "access_token": self.access_token,
                "timestamp": timestamp,
                "sign": sign
            },
            data=data,
            proxy=self.proxy_url
        )
        
        debug("dingtalk", f"发送结果: {result.status}:{result.status_text}, {result.data}")
        
        # 检查错误
        if result.data and isinstance(result.data, dict) and result.data.get("errcode") == 310000:
            warn(f"钉钉推送失败，请检查安全配置: {result.data}")
            
        return result 