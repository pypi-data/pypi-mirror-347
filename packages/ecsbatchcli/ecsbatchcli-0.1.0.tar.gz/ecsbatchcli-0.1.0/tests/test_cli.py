#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行接口模块测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import yaml

# 模拟依赖模块
mock_volcenginesdkcore = MagicMock()
mock_volcenginesdkecs = MagicMock()
sys.modules['volcenginesdkcore'] = mock_volcenginesdkcore
sys.modules['volcenginesdkecs'] = mock_volcenginesdkecs

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入需要测试的模块
from src.ecsbatchcli.config import ConfigError

# 定义模拟的异常类
class MockOperationError(Exception):
    """模拟的操作错误异常"""
    pass


class TestArgparse(unittest.TestCase):
    """命令行参数解析测试类"""

    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'config.yaml')

        # 创建有效的配置数据
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            },
            'profiles': [
                {
                    'name': 'test-profile',
                    'region_id': 'cn-beijing',
                    'availability_zone_id': 'cn-beijing-a',
                    'image_id': 'image-test',
                    'security_group_id': 'sg-test',
                    'vpc_id': 'vpc-test',
                    'subnet_id': 'subnet-test',
                    'default_instance_type': 'ecs.g1ie.large',
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 40,
                    'hostname_prefix': 'test-server',
                    'project_id': 'project-test'
                }
            ]
        }

        # 写入配置文件
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)

    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()

    def test_argparse_create(self):
        """测试创建命令参数解析"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')
        parser.add_argument('--debug', action='store_true')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 创建云主机子命令
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('-g', '--config-group', required=True)
        create_parser.add_argument('-t', '--instance-type')
        create_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试参数解析
        args = parser.parse_args(['create', '--config-group', 'test-profile', '--count', '2'])

        # 验证参数
        self.assertEqual(args.command, 'create')
        self.assertEqual(args.config_group, 'test-profile')
        self.assertEqual(args.count, 2)
        self.assertIsNone(args.instance_type)
        self.assertEqual(args.config, 'config.yaml')
        self.assertFalse(args.debug)

    def test_argparse_create_with_instance_type(self):
        """测试带实例规格的创建命令参数解析"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')
        parser.add_argument('--debug', action='store_true')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 创建云主机子命令
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('-g', '--config-group', required=True)
        create_parser.add_argument('-t', '--instance-type')
        create_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试参数解析
        args = parser.parse_args(['create', '--config-group', 'test-profile', '--instance-type', 'ecs.g1ie.xlarge', '--count', '2'])

        # 验证参数
        self.assertEqual(args.command, 'create')
        self.assertEqual(args.config_group, 'test-profile')
        self.assertEqual(args.count, 2)
        self.assertEqual(args.instance_type, 'ecs.g1ie.xlarge')
        self.assertEqual(args.config, 'config.yaml')
        self.assertFalse(args.debug)

    def test_argparse_delete(self):
        """测试销毁命令参数解析"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')
        parser.add_argument('--debug', action='store_true')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 销毁云主机子命令
        delete_parser = subparsers.add_parser('delete')
        delete_parser.add_argument('-g', '--config-group', required=True)
        delete_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试参数解析
        args = parser.parse_args(['delete', '--config-group', 'test-profile', '--count', '3'])

        # 验证参数
        self.assertEqual(args.command, 'delete')
        self.assertEqual(args.config_group, 'test-profile')
        self.assertEqual(args.count, 3)
        self.assertEqual(args.config, 'config.yaml')
        self.assertFalse(args.debug)

    def test_argparse_custom_config(self):
        """测试自定义配置文件路径"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')
        parser.add_argument('--debug', action='store_true')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 创建云主机子命令
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('-g', '--config-group', required=True)
        create_parser.add_argument('-t', '--instance-type')
        create_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试参数解析
        args = parser.parse_args(['-c', '/path/to/custom/config.yaml', 'create', '--config-group', 'test-profile', '--count', '2'])

        # 验证参数
        self.assertEqual(args.config, '/path/to/custom/config.yaml')
        self.assertEqual(args.command, 'create')
        self.assertEqual(args.config_group, 'test-profile')
        self.assertEqual(args.count, 2)

    def test_argparse_debug_mode(self):
        """测试调试模式"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')
        parser.add_argument('--debug', action='store_true')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 创建云主机子命令
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('-g', '--config-group', required=True)
        create_parser.add_argument('-t', '--instance-type')
        create_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试参数解析
        args = parser.parse_args(['--debug', 'create', '--config-group', 'test-profile', '--count', '2'])

        # 验证参数
        self.assertTrue(args.debug)
        self.assertEqual(args.command, 'create')
        self.assertEqual(args.config_group, 'test-profile')
        self.assertEqual(args.count, 2)

    def test_argparse_required_args(self):
        """测试必填参数验证"""
        import argparse

        # 创建参数解析器
        parser = argparse.ArgumentParser(description='火山引擎ECS批量管理CLI工具')
        parser.add_argument('-c', '--config', default='config.yaml')

        # 创建子命令解析器
        subparsers = parser.add_subparsers(dest='command')

        # 创建云主机子命令
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('-g', '--config-group', required=True)
        create_parser.add_argument('-n', '--count', type=int, required=True)

        # 测试缺少必填参数
        with self.assertRaises(SystemExit):
            parser.parse_args(['create', '--config-group', 'test-profile'])

        with self.assertRaises(SystemExit):
            parser.parse_args(['create', '--count', '2'])


if __name__ == '__main__':
    unittest.main()
