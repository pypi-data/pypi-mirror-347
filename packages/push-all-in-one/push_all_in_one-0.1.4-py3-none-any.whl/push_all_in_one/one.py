from typing import Dict, Any, TypeVar, Type, Literal, Union, Optional, ClassVar, Generic
from .interfaces.send import Send
from .interfaces.response import SendResponse
from .push.dingtalk import Dingtalk

# 导入所有推送服务
# 暂时只添加了钉钉，其他推送服务类似实现
# from .push import (
#     CustomEmail, Dingtalk, Discord, Feishu, IGot, Ntfy, OneBot, 
#     PushDeer, PushPlus, Qmsg, ServerChanTurbo, ServerChanV3, 
#     Telegram, WechatApp, WechatRobot, XiZhi, WxPusher
# )

# 推送类型
PushType = Literal["Dingtalk"]  # 后续添加其他类型

# 推送服务映射
PushMapping = {
    "Dingtalk": Dingtalk,
    # 后续添加其他映射
}

class PushAllInOne:
    """
    推送聚合类
    支持多种推送方式，统一接口调用
    """
    
    @staticmethod
    async def send(
        title: str,
        desp: str,
        push_type: PushType,
        config: Dict[str, Any],
        options: Optional[Dict[str, Any]] = None
    ) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息内容
            push_type: 推送类型
            config: 推送配置
            options: 推送选项
            
        Returns:
            SendResponse: 发送响应
        """
        if push_type not in PushMapping:
            raise ValueError(f"不支持的推送类型: {push_type}")
            
        push_class = PushMapping[push_type]
        push_instance = push_class(config)
        
        return await push_instance.send(title, desp, options)


async def runPushAllInOne(
    title: str,
    desp: str,
    push_config: Dict[str, Any]
) -> SendResponse:
    """
    运行推送聚合方法
    
    Args:
        title: 推送标题
        desp: 推送内容
        push_config: 推送配置，包含 type、config、option 字段
        
    Returns:
        SendResponse: 推送响应
    """
    push_type = push_config.get("type")
    config = push_config.get("config", {})
    options = push_config.get("options")
    
    if not push_type:
        raise ValueError("未指定推送类型")
        
    return await PushAllInOne.send(title, desp, push_type, config, options) 