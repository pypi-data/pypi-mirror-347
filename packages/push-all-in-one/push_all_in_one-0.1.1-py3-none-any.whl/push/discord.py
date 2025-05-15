import logging
from typing import Dict, Optional, Any, Union, TypedDict

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:discord")

class DiscordConfig(TypedDict):
    """Discord配置"""
    DISCORD_WEBHOOK: str  # Webhook Url 可在服务器设置 -> 整合 -> Webhook -> 创建 Webhook 中获取
    PROXY_URL: Optional[str]  # 代理地址

discordConfigSchema = {
    "DISCORD_WEBHOOK": {
        "type": "string",
        "title": "Webhook Url",
        "description": "Webhook Url 可在服务器设置 -> 整合 -> Webhook -> 创建 Webhook 中获取",
        "required": True,
    },
    "PROXY_URL": {
        "type": "string",
        "title": "代理地址",
        "description": "代理地址",
        "required": False,
    },
}

class DiscordOption(TypedDict, total=False):
    """
    Discord 额外选项
    由于参数过多，因此请参考官方文档进行配置
    """
    username: str  # 机器人显示的名称
    avatar_url: str  # 机器人头像的 Url

discordOptionSchema = {
    "username": {
        "type": "string",
        "title": "机器人显示的名称",
        "description": "机器人显示的名称",
        "required": False,
    },
    "avatar_url": {
        "type": "string",
        "title": "机器人头像的 Url",
        "description": "机器人头像的 Url",
        "required": False,
    },
}

class DiscordResponse(TypedDict):
    """Discord响应"""
    pass

class Discord(Send):
    """
    Discord Webhook 推送
    """
    
    namespace = "Discord"
    configSchema = discordConfigSchema
    optionSchema = discordOptionSchema
    
    def __init__(self, config: DiscordConfig):
        """
        创建 Discord 实例
        
        Args:
            config: Discord配置
        """
        self.DISCORD_WEBHOOK = config["DISCORD_WEBHOOK"]
        self.proxyUrl = config.get("PROXY_URL")
        
        logger.debug(f'DISCORD_WEBHOOK: {self.DISCORD_WEBHOOK}, PROXY_URL: {self.proxyUrl}')
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[DiscordOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息的标题
            desp: 消息的描述。最多 2000 个字符
            option: 额外选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        username = option.get("username")
        avatar_url = option.get("avatar_url")
        
        # 移除已处理的选项
        option_copy = option.copy()
        if "username" in option_copy:
            del option_copy["username"]
        if "avatar_url" in option_copy:
            del option_copy["avatar_url"]
            
        content = f"{title}"
        if desp:
            content += f"\n{desp}"
            
        data = {
            "content": content,
        }
        
        if username:
            data["username"] = username
        if avatar_url:
            data["avatar_url"] = avatar_url
            
        # 添加其他选项
        data.update(option_copy)
        
        return await ajax(
            url=self.DISCORD_WEBHOOK,
            method="POST",
            proxy_url=self.proxyUrl,
            data=data,
        ) 