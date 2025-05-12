#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
错误处理模块
"""

import sys
import traceback
import logging
from typing import Dict, Any, Optional, Type, List, Callable

from volcenginesdkcore.rest import ApiException

from .logger import log_exception
from .config import ConfigError
from .api_client import ApiClientError
from .operations import OperationError


# 错误类型映射
ERROR_TYPES = {
    ConfigError: "配置错误",
    ApiClientError: "API调用错误",
    OperationError: "操作错误",
    ApiException: "火山引擎API错误",
    ValueError: "参数错误",
    FileNotFoundError: "文件不存在",
    PermissionError: "权限错误",
    ConnectionError: "网络连接错误",
    TimeoutError: "请求超时",
    Exception: "未知错误"
}

# 错误解决方案映射
ERROR_SOLUTIONS = {
    # 配置错误
    "配置文件不存在": "请确保配置文件路径正确，或使用'--auto-create-config'参数自动创建示例配置文件",
    "配置文件格式错误": "请检查配置文件的YAML格式是否正确",
    "配置文件为空": "请确保配置文件包含必要的配置信息",
    "配置组不存在": "请检查配置组名称是否正确，或在配置文件中添加该配置组",
    "缺少必要字段": "请在配置文件中添加缺失的必要字段",
    "字段类型错误": "请确保字段值的类型正确",
    "字段值无效": "请确保字段值有效",
    
    # API调用错误
    "认证失败": "请检查访问密钥ID和访问密钥是否正确",
    "请求参数错误": "请检查请求参数是否正确",
    "资源不存在": "请检查资源ID是否正确",
    "资源已存在": "请使用其他名称或ID",
    "配额不足": "请申请更多配额或减少请求数量",
    "限流": "请减少请求频率或稍后重试",
    "API调用失败": "请检查网络连接和API参数",
    
    # 操作错误
    "未找到符合条件的云主机实例": "请检查筛选条件是否正确，或确认是否有符合条件的实例",
    "用户取消了操作": "操作已被用户取消",
    "实例规格不存在": "请检查实例规格是否正确",
    
    # 网络错误
    "网络连接错误": "请检查网络连接是否正常",
    "请求超时": "请检查网络连接是否正常，或稍后重试",
    
    # 文件错误
    "文件不存在": "请确保文件路径正确",
    "权限错误": "请确保有足够的权限访问文件",
    
    # 通用错误
    "未知错误": "请查看日志文件获取详细信息，或联系技术支持"
}


def get_error_type(error: Exception) -> str:
    """
    获取错误类型
    
    Args:
        error: 异常对象
        
    Returns:
        错误类型描述
    """
    for error_class, error_type in ERROR_TYPES.items():
        if isinstance(error, error_class):
            return error_type
    return ERROR_TYPES[Exception]


def get_error_solution(error: Exception) -> str:
    """
    获取错误解决方案
    
    Args:
        error: 异常对象
        
    Returns:
        错误解决方案
    """
    error_message = str(error).lower()
    
    # 尝试匹配错误消息中的关键词
    for keyword, solution in ERROR_SOLUTIONS.items():
        if keyword.lower() in error_message:
            return solution
    
    # 如果没有匹配到关键词，返回通用解决方案
    error_type = get_error_type(error)
    if error_type in ERROR_SOLUTIONS:
        return ERROR_SOLUTIONS[error_type]
    
    return ERROR_SOLUTIONS["未知错误"]


def format_error_message(error: Exception, debug: bool = False) -> str:
    """
    格式化错误消息
    
    Args:
        error: 异常对象
        debug: 是否为调试模式
        
    Returns:
        格式化后的错误消息
    """
    error_type = get_error_type(error)
    error_message = str(error)
    error_solution = get_error_solution(error)
    
    # 构建错误消息
    message = f"{error_type}: {error_message}"
    
    # 添加解决方案
    message += f"\n解决方案: {error_solution}"
    
    # 如果是调试模式，添加堆栈信息
    if debug:
        message += f"\n\n堆栈信息:\n{traceback.format_exc()}"
    
    return message


def handle_error(error: Exception, logger: logging.Logger, debug: bool = False) -> int:
    """
    处理错误
    
    Args:
        error: 异常对象
        logger: 日志记录器
        debug: 是否为调试模式
        
    Returns:
        错误码
    """
    # 记录错误日志
    log_exception(logger, error)
    
    # 获取错误类型和错误码
    error_type = get_error_type(error)
    error_code = get_error_code(error)
    
    # 输出错误信息
    error_message = format_error_message(error, debug)
    print(error_message, file=sys.stderr)
    
    return error_code


def get_error_code(error: Exception) -> int:
    """
    获取错误码
    
    Args:
        error: 异常对象
        
    Returns:
        错误码
    """
    # 配置错误
    if isinstance(error, ConfigError):
        return 1
    # API调用错误
    elif isinstance(error, ApiClientError):
        return 2
    # 操作错误
    elif isinstance(error, OperationError):
        return 3
    # 火山引擎API错误
    elif isinstance(error, ApiException):
        return 4
    # 参数错误
    elif isinstance(error, ValueError):
        return 5
    # 文件错误
    elif isinstance(error, (FileNotFoundError, PermissionError)):
        return 6
    # 网络错误
    elif isinstance(error, (ConnectionError, TimeoutError)):
        return 7
    # 未知错误
    else:
        return 99


def is_retryable_error(error: Exception) -> bool:
    """
    判断错误是否可重试
    
    Args:
        error: 异常对象
        
    Returns:
        是否可重试
    """
    # 网络连接错误和超时错误可重试
    if isinstance(error, (ConnectionError, TimeoutError)):
        return True
    
    # API限流错误可重试
    if isinstance(error, ApiException) and "RequestLimitExceeded" in str(error):
        return True
    
    # 其他API错误，根据错误码判断
    if isinstance(error, ApiException):
        # 5xx错误可重试
        try:
            status_code = error.status
            if status_code >= 500:
                return True
        except:
            pass
    
    return False
