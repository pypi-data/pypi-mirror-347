#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置验证测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import yaml

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 模拟依赖模块
sys.modules['volcenginesdkcore'] = MagicMock()
sys.modules['volcenginesdkecs'] = MagicMock()

from src.ecsbatchcli.config import Config, ConfigError


class TestConfigValidation(unittest.TestCase):
    """配置验证测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'config.yaml')
    
    def tearDown(self):
        """测试后清理"""
        self.temp_dir.cleanup()
    
    def test_validate_empty_config(self):
        """测试验证空配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            f.write('')
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("配置文件为空或格式错误", str(context.exception))
    
    def test_validate_missing_credentials(self):
        """测试验证缺少credentials部分的配置文件"""
        config_data = {
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("配置文件缺少'credentials'部分", str(context.exception))
    
    def test_validate_invalid_credentials_type(self):
        """测试验证credentials类型错误的配置文件"""
        config_data = {
            'credentials': [],
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'credentials'必须是一个字典", str(context.exception))
    
    def test_validate_missing_access_key(self):
        """测试验证缺少access_key_id的配置文件"""
        config_data = {
            'credentials': {
                'secret_access_key': 'test_secret'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'credentials'缺少'access_key_id'字段", str(context.exception))
    
    def test_validate_missing_secret_key(self):
        """测试验证缺少secret_access_key的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'credentials'缺少'secret_access_key'字段", str(context.exception))
    
    def test_validate_empty_access_key(self):
        """测试验证access_key_id为空的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': '',
                'secret_access_key': 'test_secret'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'credentials'中的'access_key_id'字段", str(context.exception))
        self.assertIn("必须是非空字符串", str(context.exception))
    
    def test_validate_missing_profiles(self):
        """测试验证缺少profiles部分的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("配置文件缺少'profiles'部分", str(context.exception))
    
    def test_validate_empty_profiles(self):
        """测试验证profiles为空的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'profiles'列表为空", str(context.exception))
    
    def test_validate_invalid_profile_type(self):
        """测试验证profile类型错误的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            },
            'profiles': [
                'invalid_profile'
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'profiles'中的第1项必须是一个字典", str(context.exception))
    
    def test_validate_missing_required_field(self):
        """测试验证缺少必填字段的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            },
            'profiles': [
                {
                    'name': 'test-profile',
                    'region_id': 'cn-beijing',
                    # 缺少 availability_zone_id
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("缺少必要字段'availability_zone_id'", str(context.exception))
    
    def test_validate_invalid_field_type(self):
        """测试验证字段类型错误的配置文件"""
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
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 'invalid_size',  # 应该是整数
                    'hostname_prefix': 'test-server',
                    'project_id': 'project-test'
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("'system_disk_size_gb'字段", str(context.exception))
        self.assertIn("必须是integer类型", str(context.exception))
    
    def test_validate_duplicate_profile_name(self):
        """测试验证重复的配置组名称"""
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
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 40,
                    'hostname_prefix': 'test-server',
                    'project_id': 'project-test'
                },
                {
                    'name': 'test-profile',  # 重复的名称
                    'region_id': 'cn-guangzhou',
                    'availability_zone_id': 'cn-guangzhou-a',
                    'image_id': 'image-test2',
                    'security_group_id': 'sg-test2',
                    'vpc_id': 'vpc-test2',
                    'subnet_id': 'subnet-test2',
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 60,
                    'hostname_prefix': 'test-server2',
                    'project_id': 'project-test2'
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with self.assertRaises(ConfigError) as context:
            Config(self.config_path)
        
        self.assertIn("配置组名称'test-profile'重复", str(context.exception))
    
    def test_validate_valid_config(self):
        """测试验证有效的配置文件"""
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
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 40,
                    'hostname_prefix': 'test-server',
                    'project_id': 'project-test'
                }
            ]
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        config = Config(self.config_path)
        self.assertEqual(config.get_credentials(), config_data['credentials'])
        self.assertEqual(config.get_profiles(), config_data['profiles'])


if __name__ == '__main__':
    unittest.main()
