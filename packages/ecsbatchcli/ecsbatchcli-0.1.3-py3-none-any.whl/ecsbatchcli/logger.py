#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志配置模块
"""

import os
import sys
import logging
import traceback
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any, List, Tuple


class LoggerError(Exception):
    """日志配置错误异常"""
    pass


# 默认日志格式
DEFAULT_LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
# 默认日期格式
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# 默认日志级别
DEFAULT_LOG_LEVEL = logging.INFO
# 默认日志文件大小限制（10MB）
DEFAULT_MAX_BYTES = 10 * 1024 * 1024
# 默认日志文件备份数量
DEFAULT_BACKUP_COUNT = 5
# 默认日志目录
DEFAULT_LOG_DIR = os.path.expanduser('~/.ecsbatchcli/logs')
# 默认日志文件名
DEFAULT_LOG_FILE = 'ecsbatchcli.log'


def setup_logger(
    name: str = "ecsbatchcli",
    level: int = DEFAULT_LOG_LEVEL,
    log_file: Optional[str] = None,
    console: bool = True,
    log_format: str = DEFAULT_LOG_FORMAT,
    date_format: str = DEFAULT_DATE_FORMAT,
    max_bytes: int = DEFAULT_MAX_BYTES,
    backup_count: int = DEFAULT_BACKUP_COUNT
) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径，如果为None则不记录到文件
        console: 是否输出到控制台
        log_format: 日志格式
        date_format: 日期格式
        max_bytes: 日志文件大小限制
        backup_count: 日志文件备份数量

    Returns:
        配置好的日志记录器

    Raises:
        LoggerError: 日志配置错误时抛出
    """
    try:
        # 创建日志记录器
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 清除现有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # 创建格式化器
        formatter = logging.Formatter(log_format, date_format)

        # 添加文件处理器
        if log_file:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # 使用RotatingFileHandler代替FileHandler，支持日志文件轮转
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # 添加控制台处理器
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger
    except Exception as e:
        error_msg = f"设置日志记录器失败: {e}"
        # 尝试打印错误堆栈
        traceback.print_exc()
        raise LoggerError(error_msg)


def get_logger(name: str = "ecsbatchcli") -> logging.Logger:
    """
    获取日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器
    """
    return logging.getLogger(name)


def get_default_logger(
    level: Optional[int] = None,
    log_to_file: bool = True,
    console: bool = True
) -> logging.Logger:
    """
    获取默认配置的日志记录器

    Args:
        level: 日志级别，如果为None则使用默认级别
        log_to_file: 是否记录到文件
        console: 是否输出到控制台

    Returns:
        配置好的日志记录器
    """
    # 确定日志级别
    log_level = level if level is not None else DEFAULT_LOG_LEVEL

    # 确定日志文件路径
    log_file = None
    if log_to_file:
        # 确保日志目录存在
        if not os.path.exists(DEFAULT_LOG_DIR):
            os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
        log_file = os.path.join(DEFAULT_LOG_DIR, DEFAULT_LOG_FILE)

    # 配置日志记录器
    return setup_logger(
        level=log_level,
        log_file=log_file,
        console=console
    )


def set_log_level(level: int) -> None:
    """
    设置根日志记录器的日志级别

    Args:
        level: 日志级别
    """
    root_logger = logging.getLogger('ecsbatchcli')
    root_logger.setLevel(level)
    for handler in root_logger.handlers:
        handler.setLevel(level)


def format_exception(e: Exception) -> str:
    """
    格式化异常信息

    Args:
        e: 异常对象

    Returns:
        格式化后的异常信息
    """
    return f"{type(e).__name__}: {str(e)}"


def log_exception(logger: logging.Logger, e: Exception, message: str = "发生异常") -> None:
    """
    记录异常信息

    Args:
        logger: 日志记录器
        e: 异常对象
        message: 日志消息前缀
    """
    logger.error(f"{message}: {format_exception(e)}")
    logger.debug(f"异常堆栈: {traceback.format_exc()}")


# 初始化默认日志记录器
default_logger = get_default_logger()
