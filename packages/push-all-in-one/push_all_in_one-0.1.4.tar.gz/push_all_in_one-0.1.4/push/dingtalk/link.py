from dataclasses import dataclass, field

@dataclass
class LinkContent:
    """钉钉链接消息内容"""
    text: str
    title: str
    picUrl: str = ""
    messageUrl: str = ""


@dataclass
class Link:
    """钉钉链接消息"""
    msgtype: str = "link"
    link: LinkContent = field(default_factory=LinkContent) 