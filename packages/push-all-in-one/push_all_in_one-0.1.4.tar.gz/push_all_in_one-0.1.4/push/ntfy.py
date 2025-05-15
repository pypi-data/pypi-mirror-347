import logging
import base64
import email.utils
import quopri
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:ntfy")

class NtfyConfig(TypedDict):
    """Ntfy配置"""
    NTFY_URL: str  # 推送地址
    NTFY_TOPIC: str  # 主题，用于区分不同的推送目标。主题本质上是一个密码，所以请选择不容易猜到的东西。例如：`my-topic`
    NTFY_AUTH: Optional[str]  # 认证参数。支持 Basic Auth、Bearer Token。Basic Auth 示例："Basic dGVzdDpwYXNz"。Bearer Token 示例："Bearer tk_..."

ntfyConfigSchema = {
    "NTFY_URL": {
        "type": "string",
        "title": "推送地址",
        "description": "推送地址",
        "required": True,
        "default": "",
    },
    "NTFY_TOPIC": {
        "type": "string",
        "title": "主题",
        "description": "主题",
        "required": True,
        "default": "",
    },
    "NTFY_AUTH": {
        "type": "string",
        "title": "认证参数",
        "description": "支持 Basic Auth、Bearer Token。\n" +
            "Basic Auth 示例：\"Basic dGVzdDpwYXNz\"\n" +
            "Bearer Token 示例：\"Bearer tk_...\"",
        "required": False,
        "default": "",
    },
}

class NtfyOption(TypedDict, total=False):
    """Ntfy选项"""
    title: str  # 通知中显示的标题
    message: str  # 通知中显示的消息正文
    body: str  # 消息正文
    priority: int  # 消息优先级（1-5，1最低，5最高）
    tags: str  # 标签列表（逗号分隔），支持Emoji短代码
    markdown: bool  # 启用Markdown格式化（设为`true`或`yes`）
    delay: str  # 延迟发送时间（支持时间戳、自然语言如`tomorrow 10am`）
    click: str  # 点击通知时打开的URL
    attach: str  # 附加文件的URL
    filename: str  # 附件的显示文件名
    icon: str  # 通知图标的URL（仅支持JPEG/PNG）
    actions: str  # 定义通知的操作按钮（JSON或简写格式）
    cache: bool  # 设为`no`禁止服务器缓存消息
    firebase: bool  # 设为`no`禁止转发到Firebase（仅影响Android推送）
    unifiedPush: bool  # 设为`1`启用UnifiedPush模式（用于Matrix网关）
    email: str  # 将通知转发到指定邮箱
    call: str  # 发送语音呼叫（需验证手机号，仅限认证用户）
    contentType: str  # 设为`text/markdown`启用Markdown
    file: Any  # 直接上传文件作为附件（需设置`X-Filename`）

ntfyOptionSchema = {
    "title": {
        "type": "string",
        "title": "标题",
        "description": "标题",
        "required": False,
        "default": "",
    },
    "body": {
        "type": "string",
        "title": "消息正文",
        "description": "消息正文",
        "required": False,
        "default": "",
    },
    "priority": {
        "type": "number",
        "title": "消息优先级",
        "description": "消息优先级（1-5，1最低，5最高）",
        "required": False,
        "default": 3,
    },
    "tags": {
        "type": "string",
        "title": "标签列表",
        "description": "标签列表（逗号分隔），支持Emoji短代码",
        "required": False,
        "default": "",
    },
    "markdown": {
        "type": "boolean",
        "title": "启用Markdown格式",
        "description": "启用Markdown格式（设为`true`或`yes`）",
        "required": False,
        "default": False,
    },
    "delay": {
        "type": "string",
        "title": "延迟发送时间",
        "description": "延迟发送时间（支持时间戳、自然语言如`tomorrow 10am`）",
        "required": False,
        "default": "",
    },
    "click": {
        "type": "string",
        "title": "点击通知时打开的URL",
        "description": "点击通知时打开的URL",
        "required": False,
        "default": "",
    },
    "attach": {
        "type": "string",
        "title": "附加文件的URL",
        "description": "附加文件的URL",
        "required": False,
        "default": "",
    },
    "filename": {
        "type": "string",
        "title": "附件的显示文件名",
        "description": "附件的显示文件名",
        "required": False,
        "default": "",
    },
    "icon": {
        "type": "string",
        "title": "通知图标的URL",
        "description": "通知图标的URL（仅支持JPEG/PNG）",
        "required": False,
        "default": "",
    },
    "actions": {
        "type": "string",
        "title": "定义通知的操作按钮",
        "description": "定义通知的操作按钮（JSON或简写格式）",
        "required": False,
        "default": "",
    },
    "cache": {
        "type": "boolean",
        "title": "禁止服务器缓存消息",
        "description": "设为`no`禁止服务器缓存消息",
        "required": False,
        "default": False,
    },
    "firebase": {
        "type": "boolean",
        "title": "禁止转发到Firebase",
        "description": "设为`no`禁止转发到Firebase（仅影响Android推送）",
        "required": False,
        "default": False,
    },
    "unifiedPush": {
        "type": "boolean",
        "title": "启用UnifiedPush模式",
        "description": "设为`1`启用UnifiedPush模式（用于Matrix网关）",
        "required": False,
        "default": False,
    },
    "email": {
        "type": "string",
        "title": "邮箱",
        "description": "将通知转发到指定邮箱",
        "required": False,
        "default": "",
    },
    "call": {
        "type": "string",
        "title": "发送语音呼叫",
        "description": "发送语音呼叫（需验证手机号，仅限认证用户）",
        "required": False,
        "default": "",
    },
    "contentType": {
        "type": "string",
        "title": "编码格式",
        "description": "设为`text/markdown`启用Markdown",
        "required": False,
        "default": "",
    },
    "file": {
        "type": "object",
        "title": "附件",
        "description": "直接上传文件作为附件（需设置`X-Filename`）",
        "required": False,
    },
}

class NtfyResponse(TypedDict):
    """Ntfy响应"""
    id: str  # 消息ID
    time: int  # 消息发布时间（Unix时间戳）
    expires: int  # 消息过期时间（Unix时间戳）
    event: str  # 事件类型
    topic: str  # 主题
    message: str  # 消息内容

def rfc2047_encode(text: str) -> str:
    """
    使用RFC 2047编码文本
    
    Args:
        text: 要编码的文本
        
    Returns:
        编码后的文本
    """
    if not text:
        return text
    
    # 检查是否需要编码
    needs_encoding = False
    for char in text:
        if ord(char) > 127:
            needs_encoding = True
            break
    
    if not needs_encoding:
        return text
    
    # 使用quopri编码
    encoded = quopri.encodestring(text.encode('utf-8')).decode('ascii')
    return f"=?utf-8?Q?{encoded}?="

class Ntfy(Send):
    """
    ntfy推送。
    官方文档：https://ntfy.sh/docs/publish/
    """
    
    namespace = "ntfy"
    configSchema = ntfyConfigSchema
    optionSchema = ntfyOptionSchema
    
    def __init__(self, config: NtfyConfig):
        """
        初始化Ntfy推送
        
        Args:
            config: Ntfy配置
        """
        self.NTFY_URL = config["NTFY_URL"]
        self.NTFY_TOPIC = config["NTFY_TOPIC"]
        self.NTFY_AUTH = config.get("NTFY_AUTH")
        
        logger.debug(f'set NTFY_URL: "{self.NTFY_URL}", NTFY_TOPIC: "{self.NTFY_TOPIC}", NTFY_AUTH: "{self.NTFY_AUTH}"')
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: str, option: Optional[NtfyOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 标题
            desp: 消息内容
            option: 额外选项
            
        Returns:
            发送结果
        """
        logger.debug(f'option: {option}')
        
        option = option or {}
        headers = {}
        
        # 设置认证信息
        if self.NTFY_AUTH:
            headers["Authorization"] = self.NTFY_AUTH
        
        # 设置Content-Type
        if option.get("contentType"):
            headers["Content-Type"] = option["contentType"]
        
        # 设置标题
        x_title = title or option.get("title")
        if x_title:
            headers["X-Title"] = rfc2047_encode(x_title)
        
        # 设置其他选项
        if option.get("message"):
            headers["X-Message"] = rfc2047_encode(option["message"])
        
        if option.get("priority"):
            headers["X-Priority"] = str(option["priority"])
        
        if option.get("tags"):
            headers["X-Tags"] = option["tags"]
        
        if option.get("markdown") is not None:
            headers["X-Markdown"] = str(option["markdown"]).lower()
        
        if option.get("delay"):
            headers["X-Delay"] = option["delay"]
        
        if option.get("click"):
            headers["X-Click"] = option["click"]
        
        if option.get("attach"):
            headers["X-Attach"] = option["attach"]
        
        if option.get("filename"):
            headers["X-Filename"] = option["filename"]
        
        if option.get("icon"):
            headers["X-Icon"] = option["icon"]
        
        if option.get("actions"):
            headers["X-Actions"] = option["actions"]
        
        if option.get("cache") is not None:
            headers["X-Cache"] = "yes" if option["cache"] else "no"
        
        if option.get("firebase") is not None:
            headers["X-Firebase"] = "yes" if option["firebase"] else "no"
        
        if option.get("unifiedPush") is not None:
            headers["X-UnifiedPush"] = "1" if option["unifiedPush"] else "0"
        
        if option.get("email"):
            headers["X-Email"] = option["email"]
        
        if option.get("call"):
            headers["X-Call"] = option["call"]
        
        # 处理文件上传
        if option.get("file"):
            file = option["file"]
            headers["X-Filename"] = file.name
            headers["Content-Type"] = "application/octet-stream"
            headers["Content-Length"] = str(file.size)
            headers["Content-Disposition"] = f'attachment; filename="{file.name}"'
        
        logger.debug(f'headers: {headers}')
        
        # 设置消息内容
        data = desp or option.get("body") or option.get("message") or ""
        logger.debug(f'data: "{data}"')
        
        # 构建URL
        from urllib.parse import urljoin
        url = urljoin(self.NTFY_URL, self.NTFY_TOPIC)
        
        # 发送请求
        response = await ajax(
            url=url,
            method="POST",
            headers=headers,
            data=data,
        )
        
        return response 