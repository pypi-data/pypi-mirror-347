import logging
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:xi-zhi")

class XiZhiConfig(TypedDict):
    """息知配置"""
    XI_ZHI_KEY: str  # 息知的 key，前往 https://xz.qqoq.net/#/index 获取

xiZhiConfigSchema = {
    "XI_ZHI_KEY": {
        "type": "string",
        "title": "息知的 key",
        "description": "前往 https://xz.qqoq.net/#/index 获取",
        "required": True,
    },
}

class XiZhiOption(TypedDict, total=False):
    """息知选项"""
    pass

xiZhiOptionSchema = {}

class XiZhiResponse(TypedDict):
    """息知响应"""
    code: int  # 状态码，200 表示成功
    msg: str  # 消息

class XiZhi(Send):
    """
    息知 推送，官方文档：https://xz.qqoq.net/#/index
    
    已废弃：受微信官方监管影响，息知推送已停止服务，请开发者更换其他通道
    """
    
    namespace = "息知"
    configSchema = xiZhiConfigSchema
    optionSchema = xiZhiOptionSchema
    
    def __init__(self, config: XiZhiConfig):
        """
        初始化息知推送
        
        Args:
            config: 息知配置
        """
        self.XI_ZHI_KEY = config["XI_ZHI_KEY"]
        logger.debug(f'set XI_ZHI_KEY: "{self.XI_ZHI_KEY}"')
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
    
    async def send(self, title: str, desp: Optional[str] = None, option: Optional[XiZhiOption] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息内容
            option: 额外推送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}"')
        
        return await ajax(
            url=f"https://xizhi.qqoq.net/{self.XI_ZHI_KEY}.send",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            data={
                "title": title,
                "content": desp,
            },
        ) 