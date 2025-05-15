from typing import Any, Optional
from abc import ABC, abstractmethod
from .response import SendResponse

class Send(ABC):
    """
    要求所有 push 方法都至少实现了 send 接口
    """
    proxy_url: Optional[str] = None
    
    @abstractmethod
    async def send(self, title: str, desp: Optional[str] = None, options: Any = None) -> SendResponse:
        """
        发送消息
        
        Args:
            title: 消息标题
            desp: 消息描述
            options: 发送选项
            
        Returns:
            SendResponse: 发送响应
        """
        pass 