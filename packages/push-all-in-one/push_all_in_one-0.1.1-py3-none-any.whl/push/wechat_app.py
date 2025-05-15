import logging
import time
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List, TypeVar, cast

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate
from ..utils.helper import warn

logger = logging.getLogger("push:wechat-app")

# 企业微信应用消息类型
WechatAppMsgType = Literal['text', 'markdown', 'voice', 'file', 'image', 'video', 'textcard', 'news', 'mpnews', 'miniprogram_notice', 'template_card']

class WechatAppConfig(TypedDict):
    """企业微信应用配置"""
    WECHAT_APP_CORPID: str  # 企业ID，获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid
    WECHAT_APP_SECRET: str  # 应用的凭证密钥，获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret
    WECHAT_APP_AGENTID: int  # 企业应用的id。企业内部开发，可在应用的设置页面查看

wechatAppConfigSchema = {
    "WECHAT_APP_CORPID": {
        "type": "string",
        "title": "企业ID",
        "description": "企业ID，获取方式参考：[术语说明-corpid](https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid)",
        "required": True,
        "default": "",
    },
    "WECHAT_APP_SECRET": {
        "type": "string",
        "title": "应用的凭证密钥",
        "description": "应用的凭证密钥，获取方式参考：[术语说明-secret](https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret)",
        "required": True,
        "default": "",
    },
    "WECHAT_APP_AGENTID": {
        "type": "number",
        "title": "企业应用的id",
        "description": "企业应用的id。企业内部开发，可在应用的设置页面查看",
        "required": True,
        "default": 0,
    },
}

class WechatAppBaseOption(TypedDict, total=False):
    """企业微信应用基础选项"""
    msgtype: WechatAppMsgType  # 消息类型
    safe: Literal[0, 1]  # 表示是否是保密消息，0表示可对外分享，1表示不能，默认0。
    enable_id_trans: Literal[0, 1]  # 表示是否开启id转译，0表示否，1表示是，默认0。
    enable_duplicate_check: Literal[0, 1]  # 表示是否开启重复消息检查，0表示否，1表示是，默认0
    duplicate_check_interval: int  # 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
    touser: str  # 指定接收消息的成员，成员ID列表（多个接收者用'|'分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送

class WechatAppOptionWithParty(WechatAppBaseOption):
    """带部门的企业微信应用选项"""
    toparty: str  # 指定接收消息的部门，部门ID列表，多个接收者用'|'分隔，最多支持100个。当touser为"@all"时忽略本参数

class WechatAppOptionWithTag(WechatAppBaseOption):
    """带标签的企业微信应用选项"""
    totag: str  # 指定接收消息的标签，标签ID列表，多个接收者用'|'分隔，最多支持100个。当touser为"@all"时忽略本参数

# 企业微信应用选项可以是带部门的选项或带标签的选项
WechatAppOption = Union[WechatAppOptionWithParty, WechatAppOptionWithTag]

wechatAppOptionSchema = {
    "msgtype": {
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
                "label": "Markdown",
                "value": "markdown",
            },
            {
                "label": "语音",
                "value": "voice",
            },
            {
                "label": "文件",
                "value": "file",
            },
            {
                "label": "图片",
                "value": "image",
            },
            {
                "label": "视频",
                "value": "video",
            },
            {
                "label": "图文",
                "value": "news",
            },
            {
                "label": "小程序通知",
                "value": "miniprogram_notice",
            },
            {
                "label": "模板卡片",
                "value": "template_card",
            },
        ],
    },
    "safe": {
        "type": "select",
        "title": "是否是保密消息",
        "description": "表示是否是保密消息，0表示可对外分享，1表示不能",
        "required": False,
        "options": [
            {
                "label": "否",
                "value": 0,
            },
            {
                "label": "是",
                "value": 1,
            },
        ],
    },
    "enable_id_trans": {
        "type": "select",
        "title": "是否开启id转译",
        "description": "表示是否开启id转译，0表示否，1表示是，默认0。",
        "required": False,
        "options": [
            {
                "label": "否",
                "value": 0,
            },
            {
                "label": "是",
                "value": 1,
            },
        ],
    },
    "enable_duplicate_check": {
        "type": "select",
        "title": "是否开启重复消息检查",
        "description": "表示是否开启重复消息检查，0表示否，1表示是，默认",
        "required": False,
        "options": [
            {
                "label": "否",
                "value": 0,
            },
            {
                "label": "是",
                "value": 1,
            },
        ],
    },
    "duplicate_check_interval": {
        "type": "number",
        "title": "重复消息检查的时间间隔",
        "description": "表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时",
        "required": False,
    },
    "touser": {
        "type": "string",
        "title": "指定接收消息的成员",
        "description": "指定接收消息的成员，成员ID列表（多个接收者用'|'分隔，最多支持1000个）。",
        "required": False,
    },
    "toparty": {
        "type": "string",
        "title": "指定接收消息的部门",
        "description": "指定接收消息的部门，部门ID列表，多个接收者用'|'分隔，最多支持100个。",
        "required": False,
    },
    "totag": {
        "type": "string",
        "title": "指定接收消息的标签",
        "description": "指定接收消息的标签，标签ID列表，多个接收者用'|'分隔，最多支持100个。",
        "required": False,
    },
}

class WechatAppResponse(TypedDict, total=False):
    """企业微信应用响应"""
    errcode: int  # 企业微信返回的错误码，为0表示成功，非0表示调用失败
    errmsg: str  # 错误信息
    invaliduser: str  # 非法的用户
    invalidparty: str  # 非法的部门
    invalidtag: str  # 非法的标签
    unlicenseduser: str  # 未授权的用户
    msgid: str  # 消息ID
    response_code: str  # 响应代码

class WechatApp(Send):
    """
    企业微信应用推送，文档：https://developer.work.weixin.qq.com/document/path/90664
    """

    namespace = "企业微信应用"
    configSchema = wechatAppConfigSchema
    optionSchema = wechatAppOptionSchema

    def __init__(self, config: WechatAppConfig):
        """
        初始化企业微信应用推送
        
        Args:
            config: 企业微信应用配置
        """
        logger.debug(f"config: {config}")
        self.WECHAT_APP_CORPID = config["WECHAT_APP_CORPID"]
        self.WECHAT_APP_SECRET = config["WECHAT_APP_SECRET"]
        self.WECHAT_APP_AGENTID = config["WECHAT_APP_AGENTID"]
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        
        self.ACCESS_TOKEN = None
        self.expiresTime = 0
    
    async def get_access_token(self) -> str:
        """
        获取访问令牌
        
        Returns:
            访问令牌
        """
        result = await ajax(
            url="https://qyapi.weixin.qq.com/cgi-bin/gettoken",
            query={
                "corpid": self.WECHAT_APP_CORPID,
                "corpsecret": self.WECHAT_APP_SECRET,
            },
        )
        
        data = result["data"]
        if data.get("errcode") != 0:  # 出错返回码，为0表示成功，非0表示调用失败
            raise Exception(data.get("errmsg") or "获取 access_token 失败！")
        
        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 7200)
        
        logger.debug(f"获取 access_token 成功: {access_token}")
        self.extend_expires_time(expires_in)
        
        return access_token
    
    def extend_expires_time(self, expires_in: int) -> None:
        """
        延长过期时间
        
        Args:
            expires_in: 延长的秒数
        """
        self.expiresTime = time.time() + expires_in  # 设置过期时间
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[WechatAppOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息内容，最长不超过2048个字节，超过将截断（支持id转译）
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        if not self.ACCESS_TOKEN or time.time() >= self.expiresTime:
            self.ACCESS_TOKEN = await self.get_access_token()
        
        option = option or {}
        msgtype = option.get("msgtype", "text")
        _touser = option.get("touser")
        
        # 移除已处理的选项
        option_copy = {k: v for k, v in option.items() if k != "msgtype" and k != "touser"}
        
        if not _touser:
            warn("未指定 touser，将使用 \"@all\" 向全体成员推送")
        
        sep = "\n\n" if msgtype == "markdown" else "\n"
        content = f"{title}{f'{sep}{desp}' if desp else ''}"
        touser = _touser or "@all"  # 如果没有指定 touser，则使用全体成员
        
        data = {
            "touser": touser,
            "msgtype": msgtype,
            "agentid": self.WECHAT_APP_AGENTID,
            msgtype: {
                "content": content,
            },
            **option_copy,
        }
        
        return await ajax(
            url="https://qyapi.weixin.qq.com/cgi-bin/message/send",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            query={
                "access_token": self.ACCESS_TOKEN,
            },
            data=data,
        ) 