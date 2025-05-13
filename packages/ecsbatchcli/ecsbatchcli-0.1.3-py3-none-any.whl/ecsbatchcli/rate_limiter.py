#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API调用速率限制器模块
"""

import time
import threading
from typing import Dict, List, Any, Optional

class RateLimiter:
    """API调用速率限制器"""

    def __init__(self, max_calls_per_second: int = 20):
        """
        初始化速率限制器

        Args:
            max_calls_per_second: 每秒最大调用次数，默认为20
        """
        self.max_calls_per_second = max_calls_per_second
        self.calls_timestamps = []
        self.lock = threading.Lock()

    def acquire(self):
        """
        获取调用许可

        如果当前调用频率超过限制，会阻塞直到可以调用
        """
        with self.lock:
            current_time = time.time()

            # 清理超过1秒的记录
            self.calls_timestamps = [t for t in self.calls_timestamps if current_time - t < 1.0]

            # 如果当前窗口内的调用次数已达到限制
            if len(self.calls_timestamps) >= self.max_calls_per_second:
                # 计算需要等待的时间
                oldest_call_time = min(self.calls_timestamps)
                wait_time = 1.0 - (current_time - oldest_call_time)

                if wait_time > 0:
                    # 释放锁，等待，然后重新获取锁
                    self.lock.release()
                    time.sleep(wait_time)
                    self.lock.acquire()

                    # 重新计算时间和清理记录
                    current_time = time.time()
                    self.calls_timestamps = [t for t in self.calls_timestamps if current_time - t < 1.0]

            # 记录本次调用时间
            self.calls_timestamps.append(current_time)

# 创建全局速率限制器实例
# 火山引擎API限制：单个地域下，单个账号每秒钟调用单个API接口的次数不可超过20次
# 我们设置为18次/秒，为其他可能的API调用留出余量
vpc_api_rate_limiter = RateLimiter(max_calls_per_second=15)
