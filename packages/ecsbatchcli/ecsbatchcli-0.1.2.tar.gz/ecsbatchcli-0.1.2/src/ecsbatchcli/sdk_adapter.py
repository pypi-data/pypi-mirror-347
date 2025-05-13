#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
火山引擎SDK适配器模块

此模块用于适配不同版本的火山引擎SDK，使ECSBatchCLI能够兼容不同的SDK版本。
"""

import logging
import importlib.util
from typing import Any, Dict, Optional, List, Tuple

# 配置日志
logger = logging.getLogger(__name__)

# 尝试导入火山引擎SDK
try:
    # 尝试导入新版SDK
    import volcengine
    HAS_NEW_SDK = True
    logger.info("使用新版火山引擎SDK (volcengine-python-sdk)")
except ImportError:
    HAS_NEW_SDK = False
    logger.warning("未找到新版火山引擎SDK (volcengine-python-sdk)")

# 尝试导入旧版SDK
try:
    import volcenginesdkcore
    import volcenginesdkecs
    HAS_OLD_SDK = True
    logger.info("使用旧版火山引擎SDK (volcenginesdkcore/volcenginesdkecs)")
except ImportError:
    HAS_OLD_SDK = False
    logger.warning("未找到旧版火山引擎SDK (volcenginesdkcore/volcenginesdkecs)")

# 检查是否有可用的SDK
if not HAS_NEW_SDK and not HAS_OLD_SDK:
    logger.warning("未找到任何火山引擎SDK，请安装火山引擎SDK后再使用实际功能")
    logger.warning("可以通过以下命令安装SDK: pip install volcengine-python-sdk")
    logger.warning("详细安装指南请参考: VOLCENGINE_SDK_INSTALLATION.md")

# 定义SDK异常类
class SDKException(Exception):
    """SDK异常基类"""
    pass

class SDKNotFoundError(SDKException):
    """SDK未找到异常"""
    pass

class ApiException(SDKException):
    """API调用异常"""
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message
        super().__init__(message)

# SDK适配器类
class SDKAdapter:
    """SDK适配器，用于适配不同版本的火山引擎SDK"""

    @staticmethod
    def create_ecs_client(access_key_id: str, secret_access_key: str, region_id: str) -> Any:
        """
        创建ECS客户端

        Args:
            access_key_id: 访问密钥ID
            secret_access_key: 访问密钥
            region_id: 区域ID

        Returns:
            ECS客户端实例

        Raises:
            SDKNotFoundError: 未找到SDK时抛出
        """
        if HAS_NEW_SDK:
            # 使用新版SDK创建客户端
            from volcengine.ecs.ecs_client import EcsClient
            return EcsClient(access_key_id, secret_access_key, region_id)
        elif HAS_OLD_SDK:
            # 使用旧版SDK创建客户端
            configuration = volcenginesdkcore.Configuration()
            configuration.ak = access_key_id
            configuration.sk = secret_access_key
            configuration.region = region_id
            volcenginesdkcore.Configuration.set_default(configuration)
            return volcenginesdkecs.ECSApi()
        else:
            raise SDKNotFoundError("未找到火山引擎SDK，请安装SDK后再使用")

    @staticmethod
    def create_run_instances_request(**kwargs) -> Any:
        """
        创建运行实例请求

        Args:
            **kwargs: 请求参数

        Returns:
            运行实例请求对象

        Raises:
            SDKNotFoundError: 未找到SDK时抛出
        """
        if HAS_NEW_SDK:
            # 使用新版SDK创建请求
            # 注意：新版SDK的请求参数可能与旧版不同，需要适配
            return kwargs
        elif HAS_OLD_SDK:
            # 使用旧版SDK创建请求
            # 创建网络接口配置
            req_network_interfaces = volcenginesdkecs.NetworkInterfaceForRunInstancesInput(
                security_group_ids=kwargs.get('security_group_ids'),
                subnet_id=kwargs.get('subnet_id'),
            )

            # 创建系统盘配置
            req_volumes = volcenginesdkecs.VolumeForRunInstancesInput(
                size=kwargs.get('system_disk_size_gb'),
                volume_type=kwargs.get('system_disk_type'),
            )

            # 创建实例请求
            return volcenginesdkecs.RunInstancesRequest(
                count=kwargs.get('count', 1),
                image_id=kwargs.get('image_id'),
                instance_name=kwargs.get('instance_name'),
                instance_type_id=kwargs.get('instance_type'),
                keep_image_credential=True,
                network_interfaces=[req_network_interfaces],
                volumes=[req_volumes],
                zone_id=kwargs.get('availability_zone_id'),
                project_name=kwargs.get('project_name'),
                spot_strategy="SpotAsPriceGo",
            )
        else:
            raise SDKNotFoundError("未找到火山引擎SDK，请安装SDK后再使用")

    @staticmethod
    def create_describe_instances_request(**kwargs) -> Any:
        """
        创建描述实例请求

        Args:
            **kwargs: 请求参数

        Returns:
            描述实例请求对象

        Raises:
            SDKNotFoundError: 未找到SDK时抛出
        """
        if HAS_NEW_SDK:
            # 使用新版SDK创建请求
            return kwargs
        elif HAS_OLD_SDK:
            # 使用旧版SDK创建请求
            request = volcenginesdkecs.DescribeInstancesRequest(
                page_size=kwargs.get('page_size', 50),
                page_number=kwargs.get('page_number', 1)
            )

            # 添加过滤条件
            if 'instance_name_prefix' in kwargs and kwargs['instance_name_prefix']:
                request.instance_name_prefix = kwargs['instance_name_prefix']

            if 'instance_ids' in kwargs and kwargs['instance_ids']:
                request.instance_ids = kwargs['instance_ids']

            return request
        else:
            raise SDKNotFoundError("未找到火山引擎SDK，请安装SDK后再使用")

    @staticmethod
    def create_delete_instance_request(instance_id: str) -> Any:
        """
        创建删除实例请求

        Args:
            instance_id: 实例ID

        Returns:
            删除实例请求对象

        Raises:
            SDKNotFoundError: 未找到SDK时抛出
        """
        if HAS_NEW_SDK:
            # 使用新版SDK创建请求
            return {'instance_id': instance_id}
        elif HAS_OLD_SDK:
            # 使用旧版SDK创建请求
            return volcenginesdkecs.DeleteInstanceRequest(
                instance_id=instance_id,
            )
        else:
            raise SDKNotFoundError("未找到火山引擎SDK，请安装SDK后再使用")
