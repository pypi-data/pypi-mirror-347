#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from push_all_in_one import get_push_service

# 获取钉钉推送服务
dingtalk = get_push_service("dingtalk", 
                           access_token="your_access_token", 
                           secret="your_secret")

# 获取企业微信推送服务
wechat = get_push_service("wechat_work", 
                         webhook_url="your_webhook_url")

# 获取Telegram推送服务
telegram = get_push_service("telegram",
                           bot_token="your_bot_token",
                           chat_id="your_chat_id")

# 发送文本消息
dingtalk.send_text("通过统一接口发送钉钉消息")
wechat.send_text("通过统一接口发送企业微信消息")
telegram.send_text("通过统一接口发送Telegram消息")

# 发送markdown消息 (支持的平台)
dingtalk.send_markdown(
    title="统一接口Markdown", 
    content="### 测试内容\n- 统一接口\n- 多平台支持"
)

# 批量推送示例
services = [dingtalk, wechat, telegram]
for service in services:
    try:
        service.send_text(f"批量推送测试消息到 {service.__class__.__name__}")
    except Exception as e:
        print(f"推送到 {service.__class__.__name__} 失败: {e}")
        
# 错误处理示例
try:
    invalid_service = get_push_service("unknown_service")
except ValueError as e:
    print(f"错误: {e}") 