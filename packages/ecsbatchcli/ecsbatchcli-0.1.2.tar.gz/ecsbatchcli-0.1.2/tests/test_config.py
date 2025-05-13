#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块测试
"""

import os
import pytest
import tempfile
import yaml
from src.ecsbatchcli.config import Config, ConfigError


class TestConfig:
    """配置管理类测试"""
    
    def setup_method(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, 'config.yaml')
    
    def teardown_method(self):
        """测试后清理"""
        self.temp_dir.cleanup()
    
    def test_load_config_file_not_exists(self):
        """测试加载不存在的配置文件"""
        with pytest.raises(ConfigError, match="配置文件不存在"):
            Config('non_existent_config.yaml')
    
    def test_load_config_invalid_yaml(self):
        """测试加载格式错误的配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            f.write('invalid: yaml: content:')
        
        with pytest.raises(ConfigError, match="配置文件格式错误"):
            Config(self.config_path)
    
    def test_load_config_missing_credentials(self):
        """测试缺少credentials部分的配置文件"""
        config_data = {
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ConfigError, match="配置文件缺少'credentials'部分"):
            Config(self.config_path)
    
    def test_load_config_missing_access_key(self):
        """测试缺少access_key_id的配置文件"""
        config_data = {
            'credentials': {
                'secret_access_key': 'test_secret'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ConfigError, match="'credentials'缺少'access_key_id'字段"):
            Config(self.config_path)
    
    def test_load_config_missing_secret_key(self):
        """测试缺少secret_access_key的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ConfigError, match="'credentials'缺少'secret_access_key'字段"):
            Config(self.config_path)
    
    def test_load_config_missing_profiles(self):
        """测试缺少profiles部分的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ConfigError, match="配置文件缺少'profiles'部分"):
            Config(self.config_path)
    
    def test_load_config_empty_profiles(self):
        """测试profiles为空的配置文件"""
        config_data = {
            'credentials': {
                'access_key_id': 'test_key',
                'secret_access_key': 'test_secret'
            },
            'profiles': []
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f)
        
        with pytest.raises(ConfigError, match="'profiles'必须是一个非空列表"):
            Config(self.config_path)
    
    def test_load_config_valid(self):
        """测试加载有效的配置文件"""
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
        assert config.get_credentials() == config_data['credentials']
        assert config.get_profiles() == config_data['profiles']
        assert config.get_profile_by_name('test-profile') == config_data['profiles'][0]
        assert config.get_profile_by_name('non-existent') is None
