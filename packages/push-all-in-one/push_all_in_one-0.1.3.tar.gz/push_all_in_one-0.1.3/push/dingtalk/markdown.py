from typing import Optional
from dataclasses import dataclass, field
from .text import At

@dataclass
class MarkdownContent:
    """钉钉markdown消息内容"""
    title: str
    text: str


@dataclass
class Markdown:
    """钉钉markdown消息"""
    msgtype: str = "markdown"
    markdown: MarkdownContent = field(default_factory=MarkdownContent)
    at: Optional[At] = field(default_factory=At) 