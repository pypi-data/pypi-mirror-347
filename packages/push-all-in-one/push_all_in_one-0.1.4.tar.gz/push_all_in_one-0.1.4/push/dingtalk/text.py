from typing import List, Dict, Optional
from dataclasses import dataclass, field

@dataclass
class TextContent:
    """钉钉文本消息内容"""
    content: str


@dataclass
class At:
    """@人员"""
    atMobiles: List[str] = field(default_factory=list)
    atUserIds: List[str] = field(default_factory=list)
    isAtAll: bool = False


@dataclass
class Text:
    """钉钉文本消息"""
    msgtype: str = "text"
    text: TextContent = field(default_factory=TextContent)
    at: Optional[At] = field(default_factory=At) 