#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from push_all_in_one import DingTalkPush

# 使用密钥方式
push = DingTalkPush(
    access_token="your_access_token",
    secret="your_secret"
)

# 发送文本消息
push.send_text("这是一条测试消息")

# 发送markdown消息
push.send_markdown(
    title="测试标题", 
    content="### 测试内容\n- 项目1\n- 项目2"
)

# 发送链接消息
push.send_link(
    title="这是一条链接消息", 
    text="这是链接的描述", 
    message_url="https://www.example.com", 
    pic_url="https://example.com/image.png"
)

# 发送ActionCard消息
push.send_action_card(
    title="这是一个ActionCard", 
    text="## 标题\n内容", 
    btns=[
        {"title": "按钮1", "action_url": "https://www.example.com/1"}, 
        {"title": "按钮2", "action_url": "https://www.example.com/2"}
    ]
)

# 发送FeedCard消息
push.send_feed_card([
    {
        "title": "标题1", 
        "message_url": "https://www.example.com/1", 
        "pic_url": "https://example.com/image1.png"
    },
    {
        "title": "标题2", 
        "message_url": "https://www.example.com/2", 
        "pic_url": "https://example.com/image2.png"
    }
]) 