import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.validate import validate

logger = logging.getLogger("push:custom-email")

# 邮件类型
CustomEmailType = Literal['text', 'html']

class CustomEmailConfig(TypedDict):
    """自定义邮件配置"""
    EMAIL_TYPE: CustomEmailType  # 邮件类型
    EMAIL_TO_ADDRESS: str  # 收件邮箱
    EMAIL_AUTH_USER: str  # 发件邮箱
    EMAIL_AUTH_PASS: str  # 发件授权码(或密码)
    EMAIL_HOST: str  # 发件域名
    EMAIL_PORT: int  # 发件端口

customEmailConfigSchema = {
    "EMAIL_TYPE": {
        "type": "select",
        "title": "邮件类型",
        "description": "邮件类型",
        "required": True,
        "default": "text",
        "options": [
            {
                "label": "文本",
                "value": "text",
            },
            {
                "label": "HTML",
                "value": "html",
            },
        ],
    },
    "EMAIL_TO_ADDRESS": {
        "type": "string",
        "title": "收件邮箱",
        "description": "收件邮箱",
        "required": True,
        "default": "",
    },
    "EMAIL_AUTH_USER": {
        "type": "string",
        "title": "发件邮箱",
        "description": "发件邮箱",
        "required": True,
        "default": "",
    },
    "EMAIL_AUTH_PASS": {
        "type": "string",
        "title": "发件授权码(或密码)",
        "description": "发件授权码(或密码)",
        "required": True,
        "default": "",
    },
    "EMAIL_HOST": {
        "type": "string",
        "title": "发件域名",
        "description": "发件域名",
        "required": True,
        "default": "",
    },
    "EMAIL_PORT": {
        "type": "number",
        "title": "发件端口",
        "description": "发件端口",
        "required": True,
        "default": 465,
    },
}

class CustomEmailOption(TypedDict, total=False):
    """自定义邮件选项"""
    to: str  # 收件邮箱
    from_addr: str  # 发件邮箱
    subject: str  # 邮件主题
    text: str  # 邮件内容
    html: str  # 邮件内容HTML

customEmailOptionSchema = {
    "to": {
        "type": "string",
        "title": "收件邮箱",
        "description": "收件邮箱",
        "required": False,
        "default": "",
    },
    "from_addr": {
        "type": "string",
        "title": "发件邮箱",
        "description": "发件邮箱",
        "required": False,
        "default": "",
    },
    "subject": {
        "type": "string",
        "title": "邮件主题",
        "description": "邮件主题",
        "required": False,
        "default": "",
    },
    "text": {
        "type": "string",
        "title": "邮件内容",
        "description": "邮件内容",
        "required": False,
        "default": "",
    },
    "html": {
        "type": "string",
        "title": "邮件内容",
        "description": "邮件内容",
        "required": False,
        "default": "",
    },
}

class SentMessageInfo(TypedDict):
    """发送消息信息"""
    response: str  # 响应信息

class CustomEmail(Send):
    """
    自定义邮件。官方文档: https://github.com/nodemailer/nodemailer
    Python中使用smtplib实现
    """
    
    namespace = "自定义邮件"
    configSchema = customEmailConfigSchema
    optionSchema = customEmailOptionSchema
    
    def __init__(self, config: CustomEmailConfig):
        """
        初始化自定义邮件
        
        Args:
            config: 自定义邮件配置
        """
        self.config = config
        logger.debug(f"CustomEmailConfig: {config}")
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    def __del__(self):
        """析构函数，用于释放资源"""
        pass
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[CustomEmailOption] = None) -> SendResponse:
        """
        发送邮件
        
        Args:
            title: 消息的标题
            desp: 消息的内容，支持 html
            option: 额外选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        EMAIL_TYPE = self.config["EMAIL_TYPE"]
        EMAIL_TO_ADDRESS = self.config["EMAIL_TO_ADDRESS"]
        EMAIL_AUTH_USER = self.config["EMAIL_AUTH_USER"]
        EMAIL_AUTH_PASS = self.config["EMAIL_AUTH_PASS"]
        EMAIL_HOST = self.config["EMAIL_HOST"]
        EMAIL_PORT = self.config["EMAIL_PORT"]
        
        option = option or {}
        _to = option.get("to")
        
        # 设置邮件信息
        from_addr = option.get("from_addr") or EMAIL_AUTH_USER
        to_addr = _to or EMAIL_TO_ADDRESS
        
        # 创建邮件对象
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = title
        
        # 根据类型设置内容
        if EMAIL_TYPE == "html":
            msg.attach(MIMEText(desp or "", "html", "utf-8"))
        else:
            msg.attach(MIMEText(desp or "", "plain", "utf-8"))
        
        try:
            # 连接SMTP服务器
            if EMAIL_PORT == 465:
                server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
            else:
                server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
                server.starttls()  # 使用TLS加密
            
            # 登录SMTP服务器
            server.login(EMAIL_AUTH_USER, EMAIL_AUTH_PASS)
            
            # 发送邮件
            server.sendmail(from_addr, to_addr.split(","), msg.as_string())
            
            # 关闭连接
            server.quit()
            
            response_info = SentMessageInfo(response="250 OK")
            logger.debug(f"CustomEmail Response: {response_info}")
            
            return {
                "status": 200,
                "statusText": "OK",
                "data": response_info,
                "headers": {},
            }
            
        except Exception as e:
            logger.error(f"发送邮件失败: {e}")
            response_info = SentMessageInfo(response=str(e))
            
            return {
                "status": 500,
                "statusText": "Internal Server Error",
                "data": response_info,
                "headers": {},
            } 