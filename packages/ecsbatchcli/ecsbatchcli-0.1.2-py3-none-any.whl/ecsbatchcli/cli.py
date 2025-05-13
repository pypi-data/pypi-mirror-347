#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行接口模块
"""

import argparse
import sys
import time
import logging
import traceback
from typing import Dict, Any, Optional

from . import __version__
from .config import Config, ConfigError
from .operations import Operations, OperationError
from .output import Output


def create_command(args: argparse.Namespace) -> int:
    """
    处理创建云主机命令

    Args:
        args: 命令行参数

    Returns:
        命令执行状态码，0表示成功，非0表示失败
    """
    # 配置输出设置
    Output.set_verbose(args.verbose)
    Output.set_color(not args.no_color)
    Output.set_level(Output.LEVEL_DEBUG if args.debug else Output.LEVEL_INFO)

    # 显示欢迎信息
    Output.print_banner("火山引擎ECS批量创建工具")

    try:
        # 加载配置
        Output.info(f"正在加载配置文件: {args.config}")
        try:
            config = Config(args.config)
        except ConfigError as e:
            if "配置文件不存在" in str(e):
                # 如果配置文件不存在，询问是否创建示例配置文件
                Output.warning(f"配置文件不存在: {args.config}")
                if args.auto_create_config or Output.confirm(f"是否创建示例配置文件? [y/N]: "):
                    try:
                        # 创建示例配置文件
                        temp_config = Config.__new__(Config)
                        temp_config.config_path = args.config
                        temp_config.config_data = {}
                        temp_config.create_example_config(args.config)
                        Output.success(f"已创建示例配置文件: {args.config}")
                        Output.info(f"请编辑配置文件，填入您的实际配置后再运行命令")
                        return 0
                    except Exception as create_error:
                        Output.error(f"创建示例配置文件失败: {create_error}")
                        return 1
                else:
                    Output.info(f"您可以手动创建配置文件，或使用'--auto-create-config'参数自动创建示例配置文件")
                    return 1
            else:
                # 其他配置错误
                raise

        # 获取配置组
        try:
            profile = config.get_profile_by_name(args.config_group)
            # 验证配置组是否包含创建云主机所需的所有字段
            config.validate_profile_for_create(profile)
        except ConfigError as e:
            Output.error(f"配置组错误: {e}")
            return 1

        # 创建操作对象
        operations = Operations(config)

        # 显示操作信息
        Output.info(f"准备批量创建云主机")
        Output.info(f"配置组: {args.config_group}")
        Output.info(f"实例规格: {args.instance_type or profile.get('default_instance_type', '未指定')}")
        Output.info(f"创建数量: {args.count}")

        # 如果是详细模式，显示更多配置信息
        if args.verbose:
            Output.info(f"区域: {profile['region_id']}")
            Output.info(f"可用区: {profile['availability_zone_id']}")
            Output.info(f"镜像ID: {profile['image_id']}")
            Output.info(f"安全组ID列表: {profile['security_group_ids']}")
            Output.info(f"VPC ID: {profile['vpc_id']}")
            Output.info(f"子网ID: {profile['subnet_id']}")
            Output.info(f"系统盘类型: {profile['system_disk_type']}")
            Output.info(f"系统盘大小: {profile['system_disk_size_gb']}GB")
            Output.info(f"主机名前缀: {profile['hostname_prefix']}")
            Output.info(f"项目名称: {profile['project_name']}")

        # 执行创建操作
        start_time = time.time()
        result = operations.create_instances(
            config_group_name=args.config_group,
            instance_type=args.instance_type,
            count=args.count
        )
        end_time = time.time()

        # 计算耗时
        elapsed_time = end_time - start_time
        result['elapsed_time'] = elapsed_time

        # 输出结果
        Output.print_create_result(result)

        # 根据成功/失败数量返回状态码
        return 0 if result['failed_count'] == 0 else 1

    except Exception as e:
        # 使用错误处理模块处理错误
        from .error_handler import handle_error
        from .logger import get_default_logger
        import logging

        # 获取日志记录器
        logger = get_default_logger(
            level=logging.DEBUG if args.debug else logging.INFO,
            log_to_file=True,
            console=False
        )

        # 处理错误
        return handle_error(e, logger, args.debug)


def delete_command(args: argparse.Namespace) -> int:
    """
    处理销毁云主机命令

    Args:
        args: 命令行参数

    Returns:
        命令执行状态码，0表示成功，非0表示失败
    """
    # 配置输出设置
    Output.set_verbose(args.verbose)
    Output.set_color(not args.no_color)
    Output.set_level(Output.LEVEL_DEBUG if args.debug else Output.LEVEL_INFO)

    # 显示欢迎信息
    Output.print_banner("火山引擎ECS批量销毁工具")

    try:
        # 加载配置
        Output.info(f"正在加载配置文件: {args.config}")
        try:
            config = Config(args.config)
        except ConfigError as e:
            if "配置文件不存在" in str(e):
                # 如果配置文件不存在，询问是否创建示例配置文件
                Output.warning(f"配置文件不存在: {args.config}")
                if args.auto_create_config or Output.confirm(f"是否创建示例配置文件? [y/N]: "):
                    try:
                        # 创建示例配置文件
                        temp_config = Config.__new__(Config)
                        temp_config.config_path = args.config
                        temp_config.config_data = {}
                        temp_config.create_example_config(args.config)
                        Output.success(f"已创建示例配置文件: {args.config}")
                        Output.info(f"请编辑配置文件，填入您的实际配置后再运行命令")
                        return 0
                    except Exception as create_error:
                        Output.error(f"创建示例配置文件失败: {create_error}")
                        return 1
                else:
                    Output.info(f"您可以手动创建配置文件，或使用'--auto-create-config'参数自动创建示例配置文件")
                    return 1
            else:
                # 其他配置错误
                raise

        # 获取配置组
        try:
            profile = config.get_profile_by_name(args.config_group)
            # 验证配置组是否包含销毁云主机所需的所有字段
            config.validate_profile_for_delete(profile)
        except ConfigError as e:
            Output.error(f"配置组错误: {e}")
            return 1

        # 创建操作对象
        operations = Operations(config)

        # 显示操作信息
        Output.info(f"准备批量销毁云主机")
        Output.info(f"配置组: {args.config_group}")
        Output.info(f"销毁数量: {args.count}")

        # 如果是详细模式，显示更多配置信息
        if args.verbose:
            Output.info(f"区域: {profile['region_id']}")
            Output.info(f"主机名前缀: {profile['hostname_prefix']}")
            if 'security_group_ids' in profile:
                Output.info(f"安全组ID列表: {profile['security_group_ids']}")
            if 'vpc_id' in profile:
                Output.info(f"VPC ID: {profile['vpc_id']}")
            if 'image_id' in profile:
                Output.info(f"镜像ID: {profile['image_id']}")

        # 执行销毁操作
        start_time = time.time()
        result = operations.delete_instances(
            config_group_name=args.config_group,
            count=args.count
        )
        end_time = time.time()

        # 计算耗时
        elapsed_time = end_time - start_time
        result['elapsed_time'] = elapsed_time

        # 输出结果
        Output.print_delete_result(result)

        # 根据成功/失败数量返回状态码
        return 0 if result['failed_count'] == 0 else 1

    except Exception as e:
        # 使用错误处理模块处理错误
        from .error_handler import handle_error
        from .logger import get_default_logger
        import logging

        # 获取日志记录器
        logger = get_default_logger(
            level=logging.DEBUG if args.debug else logging.INFO,
            log_to_file=True,
            console=False
        )

        # 处理错误
        return handle_error(e, logger, args.debug)


def list_command(args: argparse.Namespace) -> int:
    """
    处理查看云主机列表命令

    Args:
        args: 命令行参数

    Returns:
        命令执行状态码，0表示成功，非0表示失败
    """
    # 配置输出设置
    Output.set_verbose(args.verbose)
    Output.set_color(not args.no_color)
    Output.set_level(Output.LEVEL_DEBUG if args.debug else Output.LEVEL_INFO)

    # 显示欢迎信息
    Output.print_banner("火山引擎ECS实例列表查询工具")

    try:
        # 加载配置
        Output.info(f"正在加载配置文件: {args.config}")
        try:
            config = Config(args.config)
        except ConfigError as e:
            if "配置文件不存在" in str(e):
                # 如果配置文件不存在，询问是否创建示例配置文件
                Output.warning(f"配置文件不存在: {args.config}")
                if args.auto_create_config or Output.confirm(f"是否创建示例配置文件? [y/N]: "):
                    try:
                        # 创建示例配置文件
                        temp_config = Config.__new__(Config)
                        temp_config.config_path = args.config
                        temp_config.config_data = {}
                        temp_config.create_example_config(args.config)
                        Output.success(f"已创建示例配置文件: {args.config}")
                        Output.info(f"请编辑配置文件，填入您的实际配置后再运行命令")
                        return 0
                    except Exception as create_error:
                        Output.error(f"创建示例配置文件失败: {create_error}")
                        return 1
                else:
                    Output.info(f"您可以手动创建配置文件，或使用'--auto-create-config'参数自动创建示例配置文件")
                    return 1
            else:
                # 其他配置错误
                raise

        # 获取配置组
        try:
            profile = config.get_profile_by_name(args.config_group)
            # 验证配置组是否包含查询云主机所需的所有字段
            config.validate_profile_for_delete(profile)  # 使用与delete相同的验证逻辑
        except ConfigError as e:
            Output.error(f"配置组错误: {e}")
            return 1

        # 创建操作对象
        operations = Operations(config)

        # 显示操作信息
        Output.info(f"准备查询云主机列表")
        Output.info(f"配置组: {args.config_group}")

        # 如果指定了排序字段，显示排序信息
        if args.sort_by:
            Output.info(f"排序字段: {args.sort_by}")
            Output.info(f"排序顺序: {'升序' if args.order == 'asc' else '降序'}")

        # 如果指定了限制数量，显示限制信息
        if args.limit:
            Output.info(f"显示数量限制: {args.limit}")

        # 如果是详细模式，显示更多配置信息
        if args.verbose:
            Output.info(f"区域: {profile['region_id']}")
            Output.info(f"主机名前缀: {profile['hostname_prefix']}")
            if 'security_group_ids' in profile:
                Output.info(f"安全组ID列表: {profile['security_group_ids']}")
            if 'vpc_id' in profile:
                Output.info(f"VPC ID: {profile['vpc_id']}")
            if 'image_id' in profile:
                Output.info(f"镜像ID: {profile['image_id']}")

        # 执行查询操作
        start_time = time.time()
        result = operations.list_instances(
            config_group_name=args.config_group,
            sort_by=args.sort_by,
            order=args.order,
            limit=args.limit
        )
        end_time = time.time()

        # 计算耗时
        elapsed_time = end_time - start_time
        result['elapsed_time'] = elapsed_time

        # 输出结果
        Output.print_list_result(result, args.format)

        return 0

    except Exception as e:
        # 使用错误处理模块处理错误
        from .error_handler import handle_error
        from .logger import get_default_logger
        import logging

        # 获取日志记录器
        logger = get_default_logger(
            level=logging.DEBUG if args.debug else logging.INFO,
            log_to_file=True,
            console=False
        )

        # 处理错误
        return handle_error(e, logger, args.debug)


def main() -> int:
    """
    命令行工具主入口

    Returns:
        命令执行状态码，0表示成功，非0表示失败
    """
    # 创建命令行解析器
    parser = argparse.ArgumentParser(
        description='火山引擎ECS批量管理CLI工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 创建5台云主机
  ecsbatchcli create --config-group mining-profile --count 5

  # 使用指定实例规格创建10台云主机
  ecsbatchcli create --config-group mining-profile --instance-type ecs.g1ie.xlarge --count 10

  # 销毁3台云主机
  ecsbatchcli delete --config-group mining-profile --count 3

  # 查看云主机列表
  ecsbatchcli list --config-group mining-profile

  # 使用指定配置文件
  ecsbatchcli -c /path/to/config.yaml create --config-group mining-profile --count 5
"""
    )

    # 全局参数
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='配置文件路径，默认为当前目录下的config.yaml'
    )

    parser.add_argument(
        '--auto-create-config',
        action='store_true',
        help='如果配置文件不存在，自动创建示例配置文件'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='启用调试模式，显示详细错误信息'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='启用详细输出模式，显示更多信息'
    )

    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )

    # 创建子命令解析器
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 创建云主机子命令
    create_parser = subparsers.add_parser(
        'create',
        help='批量创建云主机',
        description='批量创建云主机，根据配置组中的参数创建指定数量的实例'
    )
    create_parser.add_argument(
        '-g', '--config-group',
        required=True,
        help='配置组名称，对应配置文件中profiles部分的name字段'
    )
    create_parser.add_argument(
        '-t', '--instance-type',
        help='实例规格，若不指定则使用配置组中的默认值'
    )
    create_parser.add_argument(
        '-n', '--count',
        type=int,
        required=True,
        help='创建实例数量'
    )

    # 销毁云主机子命令
    delete_parser = subparsers.add_parser(
        'delete',
        help='批量销毁云主机',
        description='批量销毁云主机，根据配置组中的参数筛选并销毁指定数量的实例'
    )
    delete_parser.add_argument(
        '-g', '--config-group',
        required=True,
        help='配置组名称，对应配置文件中profiles部分的name字段'
    )
    delete_parser.add_argument(
        '-n', '--count',
        type=int,
        required=True,
        help='销毁实例数量'
    )

    # 查看云主机列表子命令
    list_parser = subparsers.add_parser(
        'list',
        help='查看云主机列表',
        description='查看配置组中的云主机列表，支持排序和过滤'
    )
    list_parser.add_argument(
        '-g', '--config-group',
        required=True,
        help='配置组名称，对应配置文件中profiles部分的name字段'
    )
    list_parser.add_argument(
        '-s', '--sort-by',
        choices=['instance_id', 'instance_name', 'status', 'created_at', 'instance_type_id'],
        default='created_at',
        help='排序字段，默认按创建时间排序'
    )
    list_parser.add_argument(
        '-o', '--order',
        choices=['asc', 'desc'],
        default='asc',
        help='排序顺序，asc为升序，desc为降序，默认为升序'
    )
    list_parser.add_argument(
        '-l', '--limit',
        type=int,
        help='限制显示的实例数量，默认显示所有'
    )
    list_parser.add_argument(
        '-f', '--format',
        choices=['table', 'json'],
        default='table',
        help='输出格式，table为表格形式，json为JSON格式，默认为表格形式'
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 如果没有指定子命令，显示帮助信息
    if not args.command:
        parser.print_help()
        return 1

    # 根据子命令调用相应的处理函数
    if args.command == 'create':
        return create_command(args)
    elif args.command == 'delete':
        return delete_command(args)
    elif args.command == 'list':
        return list_command(args)
    else:
        # 这种情况理论上不会发生，因为argparse会自动处理无效的子命令
        print(f"未知命令: {args.command}")
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
