import logging
from typing import Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('push-all-in-one')

def warn(message: str) -> None:
    """
    输出警告信息
    
    Args:
        message: 警告信息
    """
    logger.warning(message)

def debug(tag: str, message: str, *args: Any) -> None:
    """
    输出调试信息
    
    Args:
        tag: 标签
        message: 消息
        args: 参数
    """
    logger.debug(f"[{tag}] {message}", *args) 