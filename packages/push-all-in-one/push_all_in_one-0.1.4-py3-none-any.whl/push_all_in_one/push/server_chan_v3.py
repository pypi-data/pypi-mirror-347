import logging
import re
from typing import Dict, Optional, Any, Union, TypedDict, Literal, List

from ..interfaces.send import Send
from ..interfaces.response import SendResponse
from ..utils.ajax import ajax
from ..utils.validate import validate

logger = logging.getLogger("push:server-chan-v3")

class ServerChanV3Config(TypedDict):
    """Server酱³配置"""
    SERVER_CHAN_V3_SENDKEY: str  # 请前往 https://sc3.ft07.com/sendkey 领取

serverChanV3ConfigSchema = {
    "SERVER_CHAN_V3_SENDKEY": {
        "type": "string",
        "title": "SENDKEY",
        "description": "请前往 https://sc3.ft07.com/sendkey 领取",
        "required": True,
    },
}

class ServerChanV3Option(TypedDict, total=False):
    """Server酱³选项"""
    tags: Union[str, List[str]]  # 标签列表，多个标签使用竖线分隔；也可以用数组格式，数组格式下不要加竖线
    short: str  # 推送消息的简短描述，用于指定消息卡片的内容部分，尤其是在推送markdown的时候

serverChanV3OptionSchema = {
    "tags": {
        "type": "array",
        "title": "标签列表",
        "description": "多个标签用数组格式",
        "required": False,
    },
    "short": {
        "type": "string",
        "title": "推送消息的简短描述",
        "description": "用于指定消息卡片的内容部分，尤其是在推送markdown的时候",
        "required": False,
    },
}

class ServerChanV3Meta(TypedDict):
    """Server酱³响应元数据"""
    android: Any
    devices: List[Any]

class ServerChanV3Data(TypedDict):
    """Server酱³响应数据"""
    pushid: str  # 推送消息的 ID
    meta: ServerChanV3Meta

class ServerChanV3Response(TypedDict):
    """Server酱³响应"""
    code: int  # 0 表示成功，其他值表示失败
    message: str
    errno: int
    data: ServerChanV3Data

class ServerChanV3(Send):
    """
    Server酱³
    文档：https://sc3.ft07.com/doc
    """
    
    namespace = "Server酱³"
    configSchema = serverChanV3ConfigSchema
    optionSchema = serverChanV3OptionSchema
    
    def __init__(self, config: ServerChanV3Config):
        """
        创建 ServerChanV3 实例
        
        Args:
            config: 配置项
        """
        self.sendkey = config["SERVER_CHAN_V3_SENDKEY"]
        logger.debug(f'set sendkey: "{self.sendkey}"')
        
        # 根据 configSchema 验证 config
        validate(config, self.configSchema)
        
        # 解析uid
        match = re.search(r'^sctp(\d+)t', self.sendkey)
        if match:
            self.uid = match.group(1)
        else:
            self.uid = ""
            
        if not self.uid:
            raise Exception("SERVER_CHAN_V3_SENDKEY 不合法！")
    
    async def send(self, title: str, desp: str = "", option: Optional[ServerChanV3Option] = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息的标题
            desp: 消息的内容，支持 Markdown
            option: 额外发送选项
            
        Returns:
            发送结果
        """
        logger.debug(f'title: "{title}", desp: "{desp}", option: {option}')
        
        option = option or {}
        
        # 处理tags参数
        if isinstance(option.get("tags"), list):
            option["tags"] = "|".join(option["tags"])
        
        # 构建数据
        data = {
            "text": title,
            "desp": desp,
            **option,
        }
        
        return await ajax(
            url=f"https://{self.uid}.push.ft07.com/send/{self.sendkey}.send",
            method="POST",
            headers={
                "Content-Type": "application/json",
            },
            data=data,
        ) 