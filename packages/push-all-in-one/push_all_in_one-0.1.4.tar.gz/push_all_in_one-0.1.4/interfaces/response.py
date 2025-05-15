from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class SendResponse:
    """发送响应"""
    headers: Optional[Dict[str, Any]] = None
    status: int = 200
    status_text: str = "OK"
    data: Any = None 