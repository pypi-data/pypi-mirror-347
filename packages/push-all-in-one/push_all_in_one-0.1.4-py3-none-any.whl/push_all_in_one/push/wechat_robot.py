import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:wechat-robot")

# 企业微信机器人消息类型
WechatRobotMsgType = Literal['text', 'markdown', 'image', 'news', 'file', 'voice', 'template_card']

class WechatRobotConfig(TypedDict):
    """企业微信机器人配置"""
    WECHAT_ROBOT_KEY: str  # 企业微信机器人的key

wechatRobotConfigSchema = {
    "WECHAT_ROBOT_KEY": {
        "type": "string",
        "title": "企业微信机器人的key",
        "description": "企业微信机器人的key",
        "required": True,
    },
}

class WechatRobotOption(TypedDict, total=False):
    """企业微信机器人选项"""
    msgtype: WechatRobotMsgType  # 消息类型

wechatRobotOptionSchema = {
    "msgtype": {
        "type": "select",
        "title": "消息类型",
        "description": "消息类型",
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
            {
                "label": "图文",
                "value": "news",
            },
            {
                "label": "文件",
                "value": "file",
            },
            {
                "label": "语音",
                "value": "voice",
            },
            {
                "label": "模板卡片",
                "value": "template_card",
            },
        ],
        "required": False,
        "default": "text",
    },
}

class WechatRobotResponse(TypedDict):
    """企业微信机器人响应"""
    errcode: int  # 企业微信机器人返回的错误码，为0表示成功，非0表示调用失败
    errmsg: str  # 错误信息

class WechatRobot(Send):
    """
    企业微信群机器人。文档: https://developer.work.weixin.qq.com/document/path/91770
    """

    namespace = "企业微信群机器人"
    configSchema = wechatRobotConfigSchema
    optionSchema = wechatRobotOptionSchema

    def __init__(self, config: WechatRobotConfig):
        """
        初始化企业微信群机器人
        
        Args:
            config: 企业微信群机器人配置
        """
        self.WECHAT_ROBOT_KEY = config["WECHAT_ROBOT_KEY"]
        logger.debug(f'set WECHAT_ROBOT_KEY: "{self.WECHAT_ROBOT_KEY}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)

    async def send(self, title: str, desp: Optional[str] = None, option: Optional[WechatRobotOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息内容。text内容，最长不超过2048个字节；markdown内容，最长不超过4096个字节；必须是utf8编码
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        option = option or {}
        msgtype = option.get("msgtype", "text")
        
        # 移除msgtype，因为它要单独处理
        if "msgtype" in option:
            option_copy = option.copy()
            del option_copy["msgtype"]
        else:
            option_copy = option
            
        sep = "\n\n" if msgtype == "markdown" else "\n"
        content = f"{title}"
        if desp:
            content += f"{sep}{desp}"
            
        data = {
            "msgtype": msgtype,
            msgtype: {"content": content},
            **option_copy,
        }
        
        return await ajax(
            url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send",
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
            query={"key": self.WECHAT_ROBOT_KEY},
            data=data,
        ) 