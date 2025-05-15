from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="push-all-in-one",
    version="0.1.2",
    author="Your Name",
    author_email="your.email@example.com",
    description="多合一推送服务，支持钉钉、企业微信、Telegram、邮件等多种推送方式",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/push-all-in-one",
    packages=[
        'push_all_in_one',
        'push_all_in_one.push',
        'push_all_in_one.utils',
        'push_all_in_one.interfaces'
    ],
    package_dir={'push_all_in_one': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords=["push", "notification", "dingtalk", "wechat", "telegram", "discord"],
) 