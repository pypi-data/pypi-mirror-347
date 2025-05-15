import hmac
import hashlib
import base64
from typing import Union

def generate_signature(timestamp: Union[int, str], secret: str, content: str = None) -> str:
    """
    生成签名
    
    Args:
        timestamp: 时间戳
        secret: 密钥
        content: 内容
    
    Returns:
        str: 签名
    """
    if content is None:
        content = f"{timestamp}\n{secret}"
    
    # 使用HMAC-SHA256算法计算签名
    hmac_code = hmac.new(
        secret.encode('utf-8'), 
        content.encode('utf-8'), 
        digestmod=hashlib.sha256
    ).digest()
    
    # 将签名转换为Base64编码
    sign = base64.b64encode(hmac_code).decode('utf-8')
    
    return sign 