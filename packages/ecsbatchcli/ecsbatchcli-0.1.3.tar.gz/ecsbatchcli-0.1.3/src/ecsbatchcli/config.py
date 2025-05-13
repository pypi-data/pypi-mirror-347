#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理模块
"""

import os
import yaml
from typing import Dict, List, Any, Optional


class ConfigError(Exception):
    """配置错误异常"""
    pass


class Config:
    """配置管理类"""

    def __init__(self, config_path: str):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config_data = {}
        self.load_config()

    def load_config(self) -> None:
        """
        加载并验证配置文件

        Raises:
            ConfigError: 配置文件不存在、格式错误或缺少必要字段时抛出
        """
        if not os.path.exists(self.config_path):
            raise ConfigError(f"配置文件不存在: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigError(f"配置文件格式错误: {e}")

        # 验证配置文件基本结构
        self._validate_config()

    def _validate_config(self) -> None:
        """
        验证配置文件的基本结构和必要字段

        Raises:
            ConfigError: 配置文件缺少必要字段或字段类型错误时抛出
        """
        # 验证配置文件是否为空
        if not self.config_data:
            raise ConfigError("配置文件为空或格式错误")

        # 验证credentials部分
        if 'credentials' not in self.config_data:
            raise ConfigError("配置文件缺少'credentials'部分")

        credentials = self.config_data['credentials']
        if not isinstance(credentials, dict):
            raise ConfigError("'credentials'必须是一个字典")

        # 验证credentials中的必要字段
        credential_fields = {
            'access_key_id': '访问密钥ID',
            'secret_access_key': '访问密钥'
        }

        for field, description in credential_fields.items():
            if field not in credentials:
                raise ConfigError(f"'credentials'缺少'{field}'字段 ({description})")

            if not credentials[field] or not isinstance(credentials[field], str):
                raise ConfigError(f"'credentials'中的'{field}'字段 ({description}) 必须是非空字符串")

        # 验证profiles部分
        if 'profiles' not in self.config_data:
            raise ConfigError("配置文件缺少'profiles'部分")

        profiles = self.config_data['profiles']
        if not isinstance(profiles, list):
            raise ConfigError("'profiles'必须是一个列表")

        if not profiles:
            raise ConfigError("'profiles'列表为空，至少需要定义一个配置组")

        # 验证每个profile的必要字段
        profile_names = set()
        for i, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                raise ConfigError(f"'profiles'中的第{i+1}项必须是一个字典")

            # 定义必要字段及其描述和类型
            required_fields = {
                'name': {'description': '配置组名称', 'type': str},
                'region_id': {'description': '区域ID', 'type': str},
                'zone_id': {'description': '可用区ID', 'type': str},
                'image_id': {'description': '镜像ID', 'type': str},
                'security_group_ids': {'description': '安全组ID列表', 'type': list},
                'vpc_id': {'description': 'VPC ID', 'type': str},
                'subnet_id': {'description': '子网ID', 'type': str},
                'system_disk_type': {'description': '系统盘类型', 'type': str},
                'system_disk_size_gb': {'description': '系统盘大小', 'type': int},
                'hostname_prefix': {'description': '主机名前缀', 'type': str},
                'project_name': {'description': '所属项目名称', 'type': str},
                'auto_renew': {'description': '是否自动续费', 'type': bool},
                'auto_renew_period': {'description': '续费时长', 'type': int},
                'spot_strategy': {'description': '抢占式实例策略', 'type': str}
            }

            # 检查必要字段是否存在
            for field, info in required_fields.items():
                if field not in profile:
                    raise ConfigError(f"'profiles'中的第{i+1}项缺少必要字段'{field}' ({info['description']})")

                # 检查字段类型
                expected_type = info['type']
                if not isinstance(profile[field], expected_type):
                    type_name = 'string' if expected_type == str else 'integer' if expected_type == int else expected_type.__name__
                    raise ConfigError(f"'profiles'中的第{i+1}项的'{field}'字段 ({info['description']}) 必须是{type_name}类型")

                # 检查字符串字段是否为空
                if expected_type == str and not profile[field]:
                    raise ConfigError(f"'profiles'中的第{i+1}项的'{field}'字段 ({info['description']}) 不能为空")

                # 检查整数字段是否为正数
                if expected_type == int and profile[field] <= 0:
                    raise ConfigError(f"'profiles'中的第{i+1}项的'{field}'字段 ({info['description']}) 必须是正整数")

            # 检查配置组名称是否重复
            if profile['name'] in profile_names:
                raise ConfigError(f"配置组名称'{profile['name']}'重复，每个配置组必须有唯一的名称")
            profile_names.add(profile['name'])

            # 检查可选字段的类型
            if 'default_instance_type' in profile and (not isinstance(profile['default_instance_type'], str) or not profile['default_instance_type']):
                raise ConfigError(f"'profiles'中的第{i+1}项的'default_instance_type'字段 (默认实例规格) 必须是非空字符串")

    def get_credentials(self) -> Dict[str, str]:
        """
        获取访问凭证

        Returns:
            包含access_key_id和secret_access_key的字典
        """
        return self.config_data['credentials']

    def get_profiles(self) -> List[Dict[str, Any]]:
        """
        获取所有配置组

        Returns:
            配置组列表
        """
        return self.config_data['profiles']

    def get_profile_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据名称获取特定配置组

        Args:
            name: 配置组名称

        Returns:
            找到的配置组字典，如果未找到则返回None

        Raises:
            ConfigError: 如果配置组名称不存在
        """
        for profile in self.get_profiles():
            if profile['name'] == name:
                return profile

        # 如果未找到配置组，提供友好的错误信息
        available_profiles = [profile['name'] for profile in self.get_profiles()]
        profiles_str = ", ".join(f"'{p}'" for p in available_profiles)
        raise ConfigError(f"配置组'{name}'不存在，可用的配置组: {profiles_str}")

    def validate_profile_for_create(self, profile: Dict[str, Any]) -> None:
        """
        验证配置组是否包含创建云主机所需的所有字段

        Args:
            profile: 配置组字典

        Raises:
            ConfigError: 如果配置组缺少创建云主机所需的字段
        """
        # 创建云主机时必须的字段
        required_fields = {
            'region_id': '区域ID',
            'zone_id': '可用区ID',
            'image_id': '镜像ID',
            'security_group_ids': '安全组ID列表',
            'vpc_id': 'VPC ID',
            'subnet_id': '子网ID',
            'system_disk_type': '系统盘类型',
            'system_disk_size_gb': '系统盘大小',
            'hostname_prefix': '主机名前缀',
            'project_name': '所属项目名称',
            'instance_type_id': '实例规格',
            'auto_renew': '是否自动续费',
            'auto_renew_period': '续费时长',
            'spot_strategy': '抢占式实例策略'
        }

        for field, description in required_fields.items():
            if field not in profile or not profile[field]:
                raise ConfigError(f"配置组'{profile['name']}'缺少创建云主机所需的字段'{field}' ({description})")

    def validate_profile_for_delete(self, profile: Dict[str, Any]) -> None:
        """
        验证配置组是否包含销毁云主机所需的所有字段

        Args:
            profile: 配置组字典

        Raises:
            ConfigError: 如果配置组缺少销毁云主机所需的字段
        """
        # 销毁云主机时必须的字段
        required_fields = {
            'region_id': '区域ID',
            'hostname_prefix': '主机名前缀'
        }

        for field, description in required_fields.items():
            if field not in profile or not profile[field]:
                raise ConfigError(f"配置组'{profile['name']}'缺少销毁云主机所需的字段'{field}' ({description})")

    def validate_profile_for_vpc(self, profile: Dict[str, Any]) -> None:
        """
        验证配置组是否包含清理网卡所需的所有字段

        Args:
            profile: 配置组字典

        Raises:
            ConfigError: 如果配置组缺少清理网卡所需的字段
        """
        # 清理网卡时必须的字段
        required_fields = {
            'region_id': '区域ID'
        }

        for field, description in required_fields.items():
            if field not in profile or not profile[field]:
                raise ConfigError(f"配置组'{profile['name']}'缺少清理网卡所需的字段'{field}' ({description})")

    def create_example_config(self, file_path: str) -> None:
        """
        创建示例配置文件

        Args:
            file_path: 示例配置文件路径

        Raises:
            ConfigError: 如果无法创建示例配置文件
        """
        example_config = {
            'credentials': {
                'access_key_id': 'your_access_key_id',
                'secret_access_key': 'your_secret_access_key'
            },
            'profiles': [
                {
                    'name': 'example-profile',
                    'region_id': 'cn-beijing',
                    'zone_id': 'cn-beijing-a',
                    'image_id': 'image-xxxxxxxxx',
                    'security_group_ids': ['sg-xxxxxxxxx'],
                    'vpc_id': 'vpc-xxxxxxxxx',
                    'subnet_id': 'subnet-xxxxxxxxx',
                    'instance_type_id': 'ecs.g1ie.large',
                    'system_disk_type': 'ESSD_PL0',
                    'system_disk_size_gb': 40,
                    'hostname_prefix': 'example-server',
                    'project_name': 'project-xxxxxxxxx',
                    'auto_renew': True,
                    'auto_renew_period': 1,
                    'spot_strategy': 'SpotAsPriceGo'
                }
            ]
        }

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("# 火山引擎ECS批量管理CLI工具配置文件\n")
                f.write("# 请修改以下配置为您的实际配置\n\n")
                yaml.dump(example_config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        except Exception as e:
            raise ConfigError(f"无法创建示例配置文件: {e}")
