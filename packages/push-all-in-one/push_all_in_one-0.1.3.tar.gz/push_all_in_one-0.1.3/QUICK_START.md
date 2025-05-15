# Push All In One 快速入门指南

## 安装

```bash
# 使用pip安装
pip install push-all-in-one
```

## 快速开始

### 1. 钉钉推送

```python
from push_all_in_one import DingTalkPush

# 初始化（使用密钥方式）
push = DingTalkPush(
    access_token="your_access_token",  # 替换为你的access_token
    secret="your_secret"               # 替换为你的secret
)

# 发送文本消息
push.send_text("这是一条钉钉测试消息")
```

### 2. 企业微信推送

```python
from push_all_in_one import WeChatWorkPush

# 初始化
push = WeChatWorkPush(webhook_url="your_webhook_url")  # 替换为你的webhook_url

# 发送文本消息
push.send_text("这是一条企业微信测试消息")
```

### 3. Telegram推送

```python
from push_all_in_one import TelegramPush

# 初始化
push = TelegramPush(
    bot_token="your_bot_token",  # 替换为你的bot_token
    chat_id="your_chat_id"       # 替换为你的chat_id
)

# 发送文本消息
push.send_text("这是一条Telegram测试消息")
```

### 4. 使用统一接口

```python
from push_all_in_one import get_push_service

# 获取钉钉推送服务
dingtalk = get_push_service("dingtalk", 
                           access_token="your_access_token", 
                           secret="your_secret")

# 获取企业微信推送服务
wechat = get_push_service("wechat_work", 
                         webhook_url="your_webhook_url")

# 发送消息
dingtalk.send_text("通过统一接口发送钉钉消息")
wechat.send_text("通过统一接口发送企业微信消息")
```

## 自定义配置

你可以通过环境变量或配置文件来管理推送服务的配置信息，避免在代码中硬编码敏感信息：

```python
import os
from dotenv import load_dotenv
from push_all_in_one import get_push_service

# 加载.env文件中的环境变量
load_dotenv()

# 使用环境变量中的配置
dingtalk = get_push_service("dingtalk", 
                           access_token=os.getenv("DINGTALK_TOKEN"), 
                           secret=os.getenv("DINGTALK_SECRET"))

# 发送消息
dingtalk.send_text("使用环境变量配置的推送消息")
```

## 错误处理

```python
try:
    # 尝试发送消息
    push.send_text("测试消息")
    print("消息发送成功")
except Exception as e:
    # 处理发送失败的情况
    print(f"消息发送失败: {e}")
```

更多详细用法请参考 [README.md](./README.md)。 