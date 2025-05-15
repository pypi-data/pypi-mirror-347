import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate
from ..utils.helper import uniq

logger = logging.getLogger("push:wx-pusher")

class WxPusherConfig(TypedDict):
    """WxPusher配置"""
    WX_PUSHER_APP_TOKEN: str  # WxPusher 的 appToken。在 https://wxpusher.zjiecode.com/admin/main/app/appToken 申请
    WX_PUSHER_UID: str  # WxPusher 的 uid。在 https://wxpusher.zjiecode.com/admin/main/wxuser/list 查看

wxPusherConfigSchema = {
    "WX_PUSHER_APP_TOKEN": {
        "type": "string",
        "title": "appToken",
        "description": "在 https://wxpusher.zjiecode.com/admin/main/app/appToken 申请",
        "required": True,
    },
    "WX_PUSHER_UID": {
        "type": "string",
        "title": "uid",
        "description": "在 https://wxpusher.zjiecode.com/admin/main/wxuser/list 查看",
        "required": True,
    },
}

class WxPusherOption(TypedDict, total=False):
    """WxPusher选项"""
    summary: str  # 消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度20，可以不传，不传默认截取content前面的内容。
    contentType: Literal[1, 2, 3]  # 内容类型 1表示文字 2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
    save: Literal[0, 1]  # 是否保存发送内容，1保存，0不保存
    topicIds: List[int]  # 主题ID，可以根据主题ID发送消息，可以在主题管理中查看主题ID
    uids: List[str]  # 发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
    url: str  # 发送url，可以不传，如果传了，则根据url弹出通知
    verifyPayload: str  # 验证负载，仅针对text消息类型有效

wxPusherOptionSchema = {
    "summary": {
        "type": "string",
        "title": "消息摘要",
        "description": "显示在微信聊天页面或者模版消息卡片上，限制长度20，可以不传，不传默认截取content前面的内容。",
        "required": False,
    },
    "contentType": {
        "type": "select",
        "title": "内容类型",
        "description": "内容类型",
        "required": False,
        "default": 1,
        "options": [
            {
                "label": "文本",
                "value": 1,
            },
            {
                "label": "HTML",
                "value": 2,
            },
            {
                "label": "Markdown",
                "value": 3,
            },
        ],
    },
    "save": {
        "type": "select",
        "title": "是否保存发送内容",
        "description": "是否保存发送内容，1保存，0不保存，默认0",
        "required": False,
        "default": 0,
        "options": [
            {
                "label": "不保存",
                "value": 0,
            },
            {
                "label": "保存",
                "value": 1,
            },
        ],
    },
    "topicIds": {
        "type": "array",
        "title": "主题ID",
        "description": "主题ID，可以根据主题ID发送消息，可以在主题管理中查看主题ID",
        "required": False,
    },
    "uids": {
        "type": "array",
        "title": "用户ID",
        "description": "发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。",
        "required": False,
    },
    "url": {
        "type": "string",
        "title": "发送url",
        "description": "发送url，可以不传，如果传了，则根据url弹出通知",
        "required": False,
    },
    "verifyPayload": {
        "type": "string",
        "title": "验证负载",
        "description": "仅针对text消息类型有效",
        "required": False,
    },
}

class WxPusherData(TypedDict):
    """WxPusher响应数据"""
    messageId: int  # 消息ID
    code: str  # 消息编码

class WxPusherResponse(TypedDict):
    """WxPusher响应"""
    success: bool  # 请求是否成功
    code: int  # 请求返回码
    msg: str  # 请求返回消息
    data: WxPusherData  # 请求返回数据

class WxPusher(Send):
    """
    WxPusher 推送。官方文档：https://wxpusher.zjiecode.com/docs
    """
    
    namespace = "WxPusher"
    configSchema = wxPusherConfigSchema
    optionSchema = wxPusherOptionSchema
    
    def __init__(self, config: WxPusherConfig):
        """
        初始化WxPusher
        
        Args:
            config: WxPusher配置
        """
        self.WX_PUSHER_APP_TOKEN = config["WX_PUSHER_APP_TOKEN"]
        self.WX_PUSHER_UID = config["WX_PUSHER_UID"]
        
        logger.debug(f'set WX_PUSHER_APP_TOKEN: "{self.WX_PUSHER_APP_TOKEN}", WX_PUSHER_UID: "{self.WX_PUSHER_UID}"')
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[WxPusherOption] = None) -> SendResponse:
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
        
        option = option or {}
        contentType = option.get("contentType", 1)
        
        # 移除已处理的选项
        option_copy = {k: v for k, v in option.items() if k != "contentType"}
        
        # 合并uids
        option_uids = option.get("uids", [])
        if not option_uids:
            option_uids = []
        uids = uniq(option_uids + [self.WX_PUSHER_UID])
        
        # 构建内容
        content = f"{title}{f'\\n{desp}' if desp else ''}"
        
        # 构建数据
        data = {
            **option_copy,
            "appToken": self.WX_PUSHER_APP_TOKEN,
            "content": content,
            "contentType": contentType,
            "uids": uids,
        }
        
        return await ajax(
            url="https://wxpusher.zjiecode.com/api/send/message",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            data=data,
        ) 