import logging
import json
import time
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:feishu")

# 飞书用户ID类型
ReceiveIdType = Literal['open_id', 'union_id', 'user_id', 'email', 'chat_id']

# 飞书消息类型
FeishuMsgType = Literal['text', 'post', 'image', 'file', 'audio', 'media', 'sticker', 'interactive', 'share_chat', 'share_user', 'system']

class FeishuConfig(TypedDict):
    """飞书配置"""
    FEISHU_APP_ID: str  # 飞书应用 ID。官方文档：https://open.feishu.cn/document/server-docs/api-call-guide/terminology#b047be0c
    FEISHU_APP_SECRET: str  # 飞书应用密钥。官方文档：https://open.feishu.cn/document/server-docs/api-call-guide/terminology#1b5fb6cd

feishuConfigSchema = {
    "FEISHU_APP_ID": {
        "type": "string",
        "title": "飞书应用 ID",
        "description": "飞书应用 ID",
        "required": True,
        "default": "",
    },
    "FEISHU_APP_SECRET": {
        "type": "string",
        "title": "飞书应用密钥",
        "description": "飞书应用密钥",
        "required": True,
        "default": "",
    },
}

class FeishuOption(TypedDict, total=False):
    """飞书消息选项"""
    receive_id_type: ReceiveIdType  # 用户 ID 类型
    receive_id: str  # 消息接收者的 ID，ID 类型与查询参数 receive_id_type 的取值一致。
    msg_type: FeishuMsgType  # 消息类型。
    content: str  # 消息内容，JSON 结构序列化后的字符串。该参数的取值与 msg_type 对应，例如 msg_type 取值为 text，则该参数需要传入文本类型的内容。
    uuid: str  # 自定义设置的唯一字符串序列，用于在发送消息时请求去重。持有相同 uuid 的请求，在 1 小时内至多成功发送一条消息。

feishuOptionSchema = {
    "receive_id_type": {
        "type": "select",
        "title": "用户 ID 类型",
        "description": "用户 ID 类型",
        "required": True,
        "options": [
            {
                "label": "open_id",
                "value": "open_id",
            },
            {
                "label": "union_id",
                "value": "union_id",
            },
            {
                "label": "user_id",
                "value": "user_id",
            },
            {
                "label": "email",
                "value": "email",
            },
            {
                "label": "chat_id",
                "value": "chat_id",
            },
        ],
    },
    "receive_id": {
        "type": "string",
        "title": "消息接收者的 ID",
        "description": "消息接收者的 ID，ID 类型与查询参数 receive_id_type 的取值一致。",
        "required": True,
    },
    "msg_type": {
        "type": "select",
        "title": "消息类型",
        "description": "消息类型",
        "required": True,
        "options": [
            {
                "label": "文本",
                "value": "text",
            },
            {
                "label": "富文本",
                "value": "post",
            },
            {
                "label": "图片",
                "value": "image",
            },
            {
                "label": "文件",
                "value": "file",
            },
            {
                "label": "语音",
                "value": "audio",
            },
            {
                "label": "视频",
                "value": "media",
            },
            {
                "label": "表情包",
                "value": "sticker",
            },
            {
                "label": "卡片",
                "value": "interactive",
            },
            {
                "label": "分享群名片",
                "value": "share_chat",
            },
            {
                "label": "分享个人名片",
                "value": "share_user",
            },
            {
                "label": "系统消息",
                "value": "system",
            },
        ],
    },
    "content": {
        "type": "string",
        "title": "消息内容",
        "description": "消息内容，JSON 结构序列化后的字符串。该参数的取值与 msg_type 对应，例如 msg_type 取值为 text，则该参数需要传入文本类型的内容。",
        "required": False,
    },
    "uuid": {
        "type": "string",
        "title": "自定义设置的唯一字符串序列",
        "description": "自定义设置的唯一字符串序列，用于在发送消息时请求去重。持有相同 uuid 的请求，在 1 小时内至多成功发送一条消息。",
        "required": False,
    },
}

class Feishu(Send):
    """
    飞书。官方文档：https://open.feishu.cn/document/home/index
    """
    
    namespace = "飞书"
    configSchema = feishuConfigSchema
    optionSchema = feishuOptionSchema
    
    def __init__(self, config: FeishuConfig):
        """
        创建飞书实例
        
        Args:
            config: 飞书配置
        """
        self.config = config
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        self.accessToken = None
        self.expiresTime = 0
        
    async def get_access_token(self):
        """
        获取飞书访问令牌
        
        Returns:
            访问令牌
        """
        FEISHU_APP_ID = self.config["FEISHU_APP_ID"]
        FEISHU_APP_SECRET = self.config["FEISHU_APP_SECRET"]
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": FEISHU_APP_ID,
            "app_secret": FEISHU_APP_SECRET,
        }
        
        result = await ajax(
            url=url,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=data,
        )
        
        data = result["data"]
        code = data.get("code")
        msg = data.get("msg")
        tenant_access_token = data.get("tenant_access_token")
        expire = data.get("expire")
        
        if code != 0:  # 出错返回码，为0表示成功，非0表示调用失败
            raise Exception(msg or "获取 tenant_access_token 失败！")
            
        self.expiresTime = time.time() + expire
        logger.debug(f"获取 tenant_access_token 成功: {tenant_access_token}")
        
        return tenant_access_token
        
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[FeishuOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息描述
            option: 额外选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        # 检查token是否过期
        if not self.accessToken or time.time() >= self.expiresTime:
            self.accessToken = await self.get_access_token()
        
        # 设置默认值
        option = option or {}
        receive_id_type = option.get("receive_id_type", "open_id")
        receive_id = option.get("receive_id")
        msg_type = option.get("msg_type", "text")
        content = option.get("content")
        uuid = option.get("uuid")
        
        # 设置数据
        data = {"receive_id": receive_id, "msg_type": msg_type, "uuid": uuid}
        
        # 如果没有提供content，则根据msg_type生成
        if not content:
            if msg_type == "text":
                data["content"] = json.dumps({
                    "text": f"{title}{f'\\n{desp}' if desp else ''}"
                })
            elif msg_type == "post":
                data["content"] = json.dumps({
                    "post": {
                        "zh_cn": {
                            "title": title,
                            "content": [
                                [
                                    {
                                        "tag": "text",
                                        "text": desp
                                    }
                                ]
                            ]
                        }
                    }
                })
            else:
                raise Exception("msg_type is required!")
        else:
            data["content"] = content
            
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        # 发送消息
        result = await ajax(
            url="https://open.feishu.cn/open-apis/im/v1/messages",
            method="POST",
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {self.accessToken}"
            },
            data=data,
            query={
                "receive_id_type": receive_id_type
            }
        )
        
        return result 