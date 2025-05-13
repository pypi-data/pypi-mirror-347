#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
输出反馈模块
"""

import sys
import time
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from colorama import init, Fore, Style, Back
from tqdm import tqdm

# 初始化colorama
init(autoreset=True)


class Output:
    """输出反馈类"""

    # 输出级别
    LEVEL_DEBUG = 0
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ERROR = 3
    LEVEL_SUCCESS = 4

    # 当前输出级别（默认为INFO）
    current_level = LEVEL_INFO

    # 是否启用彩色输出
    enable_color = True

    # 是否启用详细输出
    verbose = False

    @classmethod
    def set_level(cls, level: int) -> None:
        """
        设置输出级别

        Args:
            level: 输出级别，可选值为LEVEL_DEBUG, LEVEL_INFO, LEVEL_WARNING, LEVEL_ERROR
        """
        cls.current_level = level

    @classmethod
    def set_color(cls, enable: bool) -> None:
        """
        设置是否启用彩色输出

        Args:
            enable: 是否启用
        """
        cls.enable_color = enable

    @classmethod
    def set_verbose(cls, verbose: bool) -> None:
        """
        设置是否启用详细输出

        Args:
            verbose: 是否启用
        """
        cls.verbose = verbose

    @classmethod
    def debug(cls, message: str) -> None:
        """
        输出调试信息

        Args:
            message: 信息内容
        """
        if cls.current_level <= cls.LEVEL_DEBUG:
            prefix = f"{Fore.CYAN}[DEBUG]{Style.RESET_ALL}" if cls.enable_color else "[DEBUG]"
            print(f"{prefix} {message}")

    @classmethod
    def info(cls, message: str) -> None:
        """
        输出信息

        Args:
            message: 信息内容
        """
        if cls.current_level <= cls.LEVEL_INFO:
            prefix = f"{Fore.BLUE}[INFO]{Style.RESET_ALL}" if cls.enable_color else "[INFO]"
            print(f"{prefix} {message}")

    @classmethod
    def success(cls, message: str) -> None:
        """
        输出成功信息

        Args:
            message: 信息内容
        """
        if cls.current_level <= cls.LEVEL_SUCCESS:
            prefix = f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL}" if cls.enable_color else "[SUCCESS]"
            print(f"{prefix} {message}")

    @classmethod
    def warning(cls, message: str) -> None:
        """
        输出警告信息

        Args:
            message: 信息内容
        """
        if cls.current_level <= cls.LEVEL_WARNING:
            prefix = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL}" if cls.enable_color else "[WARNING]"
            print(f"{prefix} {message}")

    @classmethod
    def error(cls, message: str) -> None:
        """
        输出错误信息

        Args:
            message: 信息内容
        """
        if cls.current_level <= cls.LEVEL_ERROR:
            prefix = f"{Fore.RED}[ERROR]{Style.RESET_ALL}" if cls.enable_color else "[ERROR]"
            print(f"{prefix} {message}", file=sys.stderr)

    @classmethod
    def highlight(cls, message: str, color: str = Fore.CYAN) -> str:
        """
        高亮显示文本

        Args:
            message: 文本内容
            color: 颜色，默认为青色

        Returns:
            高亮后的文本
        """
        if cls.enable_color:
            return f"{color}{message}{Style.RESET_ALL}"
        return message

    @classmethod
    def create_progress_bar(cls, total: int, desc: str = "进度", unit: str = "项") -> tqdm:
        """
        创建进度条

        Args:
            total: 总数量
            desc: 描述
            unit: 单位

        Returns:
            进度条对象
        """
        return tqdm(
            total=total,
            desc=desc,
            unit=unit,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]"
        )

    @classmethod
    def format_time(cls, seconds: float) -> str:
        """
        格式化时间

        Args:
            seconds: 秒数

        Returns:
            格式化后的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.2f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.2f}分钟"
        else:
            hours = seconds / 3600
            return f"{hours:.2f}小时"

    @classmethod
    def print_create_result(cls, result: Dict[str, Any]) -> None:
        """
        输出创建结果

        Args:
            result: 创建结果统计
        """
        # 计算成功率
        success_rate = 0
        if result['total_count'] > 0:
            success_rate = (result['success_count'] / result['total_count']) * 100

        # 获取耗时
        elapsed_time = result.get('elapsed_time', 0)
        formatted_time = cls.format_time(elapsed_time)

        # 输出统计信息
        print("\n" + "="*50)
        print(f"{'创建结果统计':^50}")
        print("="*50)
        print(f"总请求数: {result['total_count']}")

        success_text = f"{result['success_count']} ({success_rate:.1f}%)"
        if cls.enable_color:
            success_text = f"{Fore.GREEN}{success_text}{Style.RESET_ALL}"
        print(f"成功数: {success_text}")

        failed_text = str(result['failed_count'])
        if cls.enable_color and result['failed_count'] > 0:
            failed_text = f"{Fore.RED}{failed_text}{Style.RESET_ALL}"
        print(f"失败数: {failed_text}")

        print(f"总耗时: {formatted_time}")
        print("-"*50)

        # 输出成功实例
        if result['success_instances']:
            print("\n成功创建的实例:")
            for i, instance in enumerate(result['success_instances'], 1):
                instance_id = instance['instance_id']
                instance_name = instance['instance_name']
                if cls.enable_color:
                    instance_id = cls.highlight(instance_id, Fore.GREEN)
                    instance_name = cls.highlight(instance_name, Fore.GREEN)
                print(f"  {i}. ID: {instance_id}, 名称: {instance_name}")

                # 如果启用详细输出，显示更多信息
                if cls.verbose and i < len(result['success_instances']):
                    print()

        # 输出失败实例
        if result['failed_instances']:
            print("\n创建失败的实例:")
            for i, instance in enumerate(result['failed_instances'], 1):
                instance_name = instance['instance_name']
                reason = instance['reason']
                if cls.enable_color:
                    instance_name = cls.highlight(instance_name, Fore.RED)
                    reason = cls.highlight(reason, Fore.RED)
                print(f"  {i}. 名称: {instance_name}")
                print(f"     原因: {reason}")

                # 如果启用详细输出，显示更多信息
                if cls.verbose and i < len(result['failed_instances']):
                    print()

        print("\n" + "="*50)

    @classmethod
    def print_delete_result(cls, result: Dict[str, Any]) -> None:
        """
        输出销毁结果

        Args:
            result: 销毁结果统计
        """
        # 计算成功率
        success_rate = 0
        if result['total_count'] > 0:
            success_rate = (result['success_count'] / result['total_count']) * 100

        # 获取耗时
        elapsed_time = result.get('elapsed_time', 0)
        formatted_time = cls.format_time(elapsed_time)

        # 输出统计信息
        print("\n" + "="*50)
        print(f"{'销毁结果统计':^50}")
        print("="*50)
        print(f"总请求数: {result['total_count']}")

        success_text = f"{result['success_count']} ({success_rate:.1f}%)"
        if cls.enable_color:
            success_text = f"{Fore.GREEN}{success_text}{Style.RESET_ALL}"
        print(f"成功数: {success_text}")

        failed_text = str(result['failed_count'])
        if cls.enable_color and result['failed_count'] > 0:
            failed_text = f"{Fore.RED}{failed_text}{Style.RESET_ALL}"
        print(f"失败数: {failed_text}")

        print(f"总耗时: {formatted_time}")
        print("-"*50)

        # 输出成功实例
        if result['success_instances']:
            print("\n成功销毁的实例:")
            for i, instance in enumerate(result['success_instances'], 1):
                instance_id = instance['instance_id']
                instance_name = instance.get('instance_name', 'N/A')
                created_at = instance.get('created_at', 'N/A')

                if cls.enable_color:
                    instance_id = cls.highlight(instance_id, Fore.GREEN)
                    instance_name = cls.highlight(instance_name, Fore.GREEN)

                print(f"  {i}. ID: {instance_id}, 名称: {instance_name}")
                if cls.verbose:
                    print(f"     创建时间: {created_at}")
                    if i < len(result['success_instances']):
                        print()

        # 输出失败实例
        if result['failed_instances']:
            print("\n销毁失败的实例:")
            for i, instance in enumerate(result['failed_instances'], 1):
                instance_id = instance['instance_id']
                instance_name = instance.get('instance_name', 'N/A')
                reason = instance['reason']

                if cls.enable_color:
                    instance_id = cls.highlight(instance_id, Fore.RED)
                    instance_name = cls.highlight(instance_name, Fore.RED)
                    reason = cls.highlight(reason, Fore.RED)

                print(f"  {i}. ID: {instance_id}, 名称: {instance_name}")
                print(f"     原因: {reason}")

                if cls.verbose and 'created_at' in instance:
                    print(f"     创建时间: {instance['created_at']}")
                    if i < len(result['failed_instances']):
                        print()

        print("\n" + "="*50)

    @classmethod
    def confirm_delete(cls, instances: List[Dict[str, Any]]) -> bool:
        """
        确认销毁实例

        Args:
            instances: 待销毁的实例列表

        Returns:
            用户是否确认销毁
        """
        # 输出警告信息
        warning_text = "警告: 以下实例将被销毁，此操作不可逆!"
        if cls.enable_color:
            warning_text = f"{Fore.YELLOW}{Back.BLACK}{warning_text}{Style.RESET_ALL}"

        print("\n" + "!"*len(warning_text))
        print(warning_text)
        print("!"*len(warning_text))

        # 输出实例列表
        print("\n待销毁的实例列表:")
        print("-"*50)
        for i, instance in enumerate(instances, 1):
            instance_id = instance.get('instance_id', 'N/A')
            instance_name = instance.get('instance_name', 'N/A')
            created_at = instance.get('created_at', 'N/A')

            if cls.enable_color:
                instance_id = cls.highlight(instance_id, Fore.YELLOW)
                instance_name = cls.highlight(instance_name, Fore.YELLOW)

            print(f"  {i}. ID: {instance_id}")
            print(f"     名称: {instance_name}")
            print(f"     创建时间: {created_at}")

            if i < len(instances):
                print()

        print("-"*50)
        print(f"总计: {len(instances)}个实例")

        # 请求确认
        return cls.confirm("\n是否确认销毁以上实例? 输入'yes'确认: ")

    @classmethod
    def confirm(cls, prompt: str) -> bool:
        """
        通用确认方法

        Args:
            prompt: 提示信息

        Returns:
            用户是否确认
        """
        if cls.enable_color:
            prompt = f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}"

        response = input(prompt)
        return response.lower() in ('y', 'yes')

    @classmethod
    def print_banner(cls, title: str) -> None:
        """
        打印横幅

        Args:
            title: 标题
        """
        width = 60
        padding = (width - len(title)) // 2

        banner = f"\n{'#' * width}\n"
        banner += f"{'#' * padding} {title} {'#' * (width - padding - len(title) - 1)}\n"
        banner += f"{'#' * width}\n"

        if cls.enable_color:
            banner = f"{Fore.CYAN}{banner}{Style.RESET_ALL}"

        print(banner)

    @classmethod
    def print_list_result(cls, result: Dict[str, Any], format_type: str = 'table') -> None:
        """
        输出实例列表查询结果

        Args:
            result: 查询结果统计
            format_type: 输出格式，table为表格形式，json为JSON格式，默认为table
        """
        # 获取耗时
        elapsed_time = result.get('elapsed_time', 0)
        formatted_time = cls.format_time(elapsed_time)

        # 获取实例列表
        instances = result.get('instances', [])
        total_count = result.get('total_count', 0)
        sort_by = result.get('sort_by', 'created_at')
        order = result.get('order', 'asc')
        limit = result.get('limit')

        # 如果是JSON格式，直接输出JSON
        if format_type == 'json':
            import json
            # 移除不需要的字段
            result_copy = result.copy()
            if 'elapsed_time' in result_copy:
                del result_copy['elapsed_time']

            # 格式化输出JSON
            print(json.dumps(result_copy, indent=2, ensure_ascii=False))
            return

        # 输出统计信息
        print("\n" + "="*80)
        print(f"{'云主机实例列表':^80}")
        print("="*80)
        print(f"总实例数: {total_count}")
        print(f"排序字段: {sort_by}")
        print(f"排序顺序: {'升序' if order == 'asc' else '降序'}")
        if limit:
            print(f"显示数量限制: {limit}")
        print(f"查询耗时: {formatted_time}")
        print("-"*80)

        # 如果没有实例，输出提示信息
        if not instances:
            print("\n未找到符合条件的云主机实例")
            print("\n" + "="*80)
            return

        # 输出实例列表（表格形式）
        # 定义表头
        headers = ["序号", "实例ID", "实例名称", "状态", "创建时间", "实例规格"]

        # 计算每列的最大宽度
        col_widths = [4, 20, 30, 10, 20, 15]  # 初始宽度

        # 根据实际数据调整列宽
        for instance in instances:
            col_widths[1] = max(col_widths[1], len(instance.get('instance_id', '')))
            col_widths[2] = max(col_widths[2], len(instance.get('instance_name', '')))
            col_widths[3] = max(col_widths[3], len(instance.get('status', '')))
            col_widths[4] = max(col_widths[4], len(str(instance.get('created_at', ''))))
            col_widths[5] = max(col_widths[5], len(instance.get('instance_type_id', '')))

        # 打印表头
        header_row = ""
        for i, header in enumerate(headers):
            header_row += f"{header:{col_widths[i]}} | "
        print("\n" + header_row)
        print("-" * (sum(col_widths) + len(headers) * 3))

        # 打印实例数据
        for i, instance in enumerate(instances, 1):
            instance_id = instance.get('instance_id', 'N/A')
            instance_name = instance.get('instance_name', 'N/A')
            status = instance.get('status', 'N/A')
            created_at = instance.get('creation_time', instance.get('created_at', 'N/A'))  # 兼容两种字段名
            instance_type = instance.get('instance_type_id', instance.get('instance_type', 'N/A'))  # 兼容两种字段名

            # 根据状态设置颜色
            status_color = Fore.WHITE
            if status == 'RUNNING':
                status_color = Fore.GREEN
            elif status == 'STOPPED':
                status_color = Fore.YELLOW
            elif status == 'PENDING':
                status_color = Fore.BLUE
            elif status == 'TERMINATING' or status == 'TERMINATED':
                status_color = Fore.RED

            # 格式化状态文本
            status_text = status
            if cls.enable_color:
                status_text = f"{status_color}{status}{Style.RESET_ALL}"

            # 打印行
            row = f"{i:<{col_widths[0]}} | "
            row += f"{instance_id:{col_widths[1]}} | "
            row += f"{instance_name:{col_widths[2]}} | "
            row += f"{status_text:{col_widths[3] + (0 if cls.enable_color else 0)}} | "
            row += f"{created_at:{col_widths[4]}} | "
            row += f"{instance_type:{col_widths[5]}}"
            print(row)

        # 如果启用详细输出，显示更多信息
        if cls.verbose:
            print("\n详细信息:")
            for i, instance in enumerate(instances, 1):
                print(f"\n实例 {i}:")
                for key, value in instance.items():
                    if key not in ['instance_id', 'instance_name', 'status', 'created_at', 'instance_type_id']:
                        print(f"  {key}: {value}")

        print("\n" + "="*80)
