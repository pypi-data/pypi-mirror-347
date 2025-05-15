import json
from typing import Dict, Any, Optional, Union
import requests
import httpx
from ..interfaces.response import SendResponse

def request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    query: Optional[Dict[str, Any]] = None,
    data: Any = None,
    timeout: int = 30,
    proxy: Optional[str] = None
) -> SendResponse:
    """
    发送HTTP请求
    
    Args:
        url: 请求URL
        method: 请求方法
        headers: 请求头
        query: 查询参数
        data: 请求数据
        timeout: 超时时间（秒）
        proxy: 代理URL
    
    Returns:
        SendResponse: 响应对象
    """
    proxies = None
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy
        }
    
    _headers = {
        "User-Agent": "push-all-in-one/0.1.0 Python"
    }
    if headers:
        _headers.update(headers)
    
    kwargs = {
        "headers": _headers,
        "params": query,
        "timeout": timeout,
        "proxies": proxies
    }
    
    if method.upper() in ["POST", "PUT", "PATCH"]:
        if isinstance(data, dict):
            if headers and headers.get("Content-Type") == "application/json":
                kwargs["json"] = data
            else:
                kwargs["data"] = data
        else:
            kwargs["data"] = data
    
    response = requests.request(method.upper(), url, **kwargs)
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = response.text
    
    return SendResponse(
        headers=dict(response.headers),
        status=response.status_code,
        status_text=response.reason,
        data=response_data
    )

async def async_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    query: Optional[Dict[str, Any]] = None,
    data: Any = None,
    timeout: int = 30,
    proxy: Optional[str] = None
) -> SendResponse:
    """
    异步发送HTTP请求
    
    Args:
        url: 请求URL
        method: 请求方法
        headers: 请求头
        query: 查询参数
        data: 请求数据
        timeout: 超时时间（秒）
        proxy: 代理URL
    
    Returns:
        SendResponse: 响应对象
    """
    _headers = {
        "User-Agent": "push-all-in-one/0.1.0 Python"
    }
    if headers:
        _headers.update(headers)
    
    async with httpx.AsyncClient(proxies=proxy, timeout=timeout) as client:
        kwargs = {
            "headers": _headers,
            "params": query
        }
        
        if method.upper() in ["POST", "PUT", "PATCH"]:
            if isinstance(data, dict):
                if headers and headers.get("Content-Type") == "application/json":
                    kwargs["json"] = data
                else:
                    kwargs["data"] = data
            else:
                kwargs["data"] = data
        
        response = await client.request(method.upper(), url, **kwargs)
        
        try:
            response_data = response.json()
        except ValueError:
            response_data = response.text
        
        return SendResponse(
            headers=dict(response.headers),
            status=response.status_code,
            status_text=response.reason_phrase,
            data=response_data
        ) 