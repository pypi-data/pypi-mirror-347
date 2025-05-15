from typing import List
from dataclasses import dataclass, field

@dataclass
class Link:
    """链接"""
    title: str
    messageURL: str
    picURL: str


@dataclass
class FeedCardContent:
    """FeedCard内容"""
    links: List[Link] = field(default_factory=list)


@dataclass
class FeedCard:
    """钉钉信息卡片"""
    msgtype: str = "feedCard"
    feedCard: FeedCardContent = field(default_factory=FeedCardContent) 