#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
火山引擎API客户端模块
"""

import time
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

import volcenginesdkcore
import volcenginesdkecs
from volcenginesdkcore.rest import ApiException

# 配置日志
logger = logging.getLogger(__name__)


class ApiClientError(Exception):
    """API客户端错误异常"""
    pass


class EcsApiClient:
    """火山引擎ECS API客户端"""

    # 最大重试次数
    MAX_RETRIES = 3
    # 重试间隔（秒）
    RETRY_INTERVAL = 2
    # 每页查询实例数量
    PAGE_SIZE = 50

    def __init__(self, access_key_id: str, secret_access_key: str, region_id: str):
        """
        初始化API客户端

        Args:
            access_key_id: 访问密钥ID
            secret_access_key: 访问密钥
            region_id: 区域ID
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_id = region_id
        self.api_instance = self._init_api_instance()
        logger.debug(f"初始化EcsApiClient，区域: {region_id}")

    def _init_api_instance(self) -> volcenginesdkecs.ECSApi:
        """
        初始化API实例

        Returns:
            ECS API实例
        """
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = self.access_key_id
        configuration.sk = self.secret_access_key
        configuration.region = self.region_id
        volcenginesdkcore.Configuration.set_default(configuration)

        return volcenginesdkecs.ECSApi()

    def _retry_api_call(self, func, *args, **kwargs) -> Any:
        """
        带重试机制的API调用

        Args:
            func: 要调用的API函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            API调用结果

        Raises:
            ApiClientError: 重试后仍然失败时抛出
        """
        last_exception = None
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.debug(f"API调用尝试 {attempt}/{self.MAX_RETRIES}")
                return func(*args, **kwargs)
            except ApiException as e:
                last_exception = e
                # 解析错误信息
                error_code = getattr(e, 'status', None)
                error_message = str(e)

                # 记录详细错误信息
                logger.warning(f"API调用失败 (尝试 {attempt}/{self.MAX_RETRIES}): 错误码={error_code}, 错误信息={error_message}")

                # 判断是否需要重试
                if attempt < self.MAX_RETRIES:
                    # 判断错误类型
                    retryable = False

                    # 服务器错误（5xx）可重试
                    if error_code and 500 <= error_code < 600:
                        retryable = True
                        logger.info(f"服务器错误 (5xx)，将进行重试")

                    # 限流错误可重试
                    elif any(keyword in error_message for keyword in ["RequestLimitExceeded", "Throttling"]):
                        retryable = True
                        logger.info(f"API限流，将进行重试")

                    # 临时错误可重试
                    elif any(keyword in error_message for keyword in ["InternalError", "ServiceUnavailable"]):
                        retryable = True
                        logger.info(f"临时服务错误，将进行重试")

                    # 如果可重试，等待后重试
                    if retryable:
                        # 对于限流错误，使用指数退避
                        if any(keyword in error_message for keyword in ["RequestLimitExceeded", "Throttling"]):
                            wait_time = self.RETRY_INTERVAL * (2 ** (attempt - 1))  # 指数退避
                            logger.info(f"API限流，等待 {wait_time} 秒后重试")
                            time.sleep(wait_time)
                        else:
                            # 其他错误使用固定间隔
                            logger.info(f"等待 {self.RETRY_INTERVAL} 秒后重试")
                            time.sleep(self.RETRY_INTERVAL)
                    else:
                        # 不可重试的错误，直接抛出
                        error_detail = f"错误码: {error_code}, 错误信息: {error_message}"
                        logger.error(f"不可重试的API错误: {error_detail}")
                        raise ApiClientError(f"API调用失败 (不可重试): {error_detail}")

            except ConnectionError as e:
                # 网络连接错误，可重试
                last_exception = e
                logger.warning(f"网络连接错误 (尝试 {attempt}/{self.MAX_RETRIES}): {e}")

                if attempt < self.MAX_RETRIES:
                    wait_time = self.RETRY_INTERVAL * (2 ** (attempt - 1))  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

            except TimeoutError as e:
                # 超时错误，可重试
                last_exception = e
                logger.warning(f"请求超时 (尝试 {attempt}/{self.MAX_RETRIES}): {e}")

                if attempt < self.MAX_RETRIES:
                    wait_time = self.RETRY_INTERVAL * (2 ** (attempt - 1))  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)

            except Exception as e:
                # 其他未知错误，记录详细信息但不重试
                logger.error(f"API调用时发生未知错误: {e}")
                logger.debug(f"错误堆栈: {traceback.format_exc()}")
                raise ApiClientError(f"API调用时发生未知错误: {e}")

        # 所有重试都失败
        error_msg = f"API调用失败，已重试 {self.MAX_RETRIES} 次: {last_exception}"
        logger.error(error_msg)
        raise ApiClientError(error_msg)

    def create_instances(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建云主机实例

        Args:
            params: 创建实例的参数，包括：
                - availability_zone_id: 可用区ID
                - image_id: 镜像ID
                - instance_type: 实例规格
                - security_group_id: 安全组ID
                - subnet_id: 子网ID
                - vpc_id: VPC ID
                - system_disk_type: 系统盘类型
                - system_disk_size_gb: 系统盘大小（GB）
                - hostname_prefix: 主机名前缀
                - count: 创建数量
                - project_id: 项目ID

        Returns:
            API响应结果，包含创建的实例ID列表

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            count = params.get('count', 1)
            logger.info(f"开始创建云主机，数量: {count}")

            # 生成实例名称（主机名前缀 + 时间戳）
            timestamp = datetime.now().strftime("%m%d%H%M%S")
            instance_name = f"{params['hostname_prefix']}-{timestamp}"

            # 创建网络接口配置
            req_network_interfaces = volcenginesdkecs.NetworkInterfaceForRunInstancesInput(
                security_group_ids=[params['security_group_id']],
                subnet_id=params['subnet_id'],
            )

            # 创建系统盘配置
            req_volumes = volcenginesdkecs.VolumeForRunInstancesInput(
                size=params['system_disk_size_gb'],
                volume_type=params['system_disk_type'],
            )

            # 创建实例请求
            run_instances_request = volcenginesdkecs.RunInstancesRequest(
                # 购买数量
                count=count,
                # 镜像ID
                image_id=params['image_id'],
                # 实例名称
                instance_name=instance_name,
                # 实例规格
                instance_type_id=params['instance_type'],
                # 保留镜像登录凭证
                keep_image_credential=True,
                # 网络接口
                network_interfaces=[req_network_interfaces],
                # 系统盘
                volumes=[req_volumes],
                # 可用区ID
                zone_id=params['availability_zone_id'],
                # 项目ID
                project_id=params['project_id'],
                # 竞价策略
                spot_strategy="SpotAsPriceGo",
            )

            # 调用API创建实例
            logger.debug(f"调用RunInstances API，请求参数: {run_instances_request}")
            response = self._retry_api_call(
                self.api_instance.run_instances,
                run_instances_request
            )

            logger.info(f"云主机创建成功，实例ID: {response.instance_ids}")
            return {
                'instance_ids': response.instance_ids,
                'instance_name': instance_name,
                'request_id': response.request_id
            }

        except ApiException as e:
            error_msg = f"创建实例失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"创建实例时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def describe_instances(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        查询云主机实例

        Args:
            filters: 查询过滤条件，可包括：
                - hostname_prefix: 主机名前缀
                - security_group_id: 安全组ID
                - vpc_id: VPC ID
                - image_id: 镜像ID
                - instance_ids: 实例ID列表

        Returns:
            实例列表，每个实例包含ID、名称、创建时间等信息

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始查询云主机，过滤条件: {filters}")

            # 构建查询请求
            request = volcenginesdkecs.DescribeInstancesRequest(
                page_size=self.PAGE_SIZE,
                page_number=1
            )

            # 添加过滤条件
            if 'hostname_prefix' in filters and filters['hostname_prefix']:
                # 使用实例名称前缀过滤
                request.instance_name_prefix = filters['hostname_prefix']

            if 'instance_ids' in filters and filters['instance_ids']:
                # 使用实例ID列表过滤
                request.instance_ids = filters['instance_ids']

            # 调用API查询实例
            logger.debug(f"调用DescribeInstances API，请求参数: {request}")

            all_instances = []
            total_count = 0

            # 分页查询所有实例
            while True:
                response = self._retry_api_call(
                    self.api_instance.describe_instances,
                    request
                )

                if not response.instances:
                    break

                # 记录总数
                total_count = response.total_count

                # 进一步过滤实例
                for instance in response.instances:
                    # 转换为字典格式
                    instance_dict = {
                        'instance_id': instance.instance_id,
                        'instance_name': instance.instance_name,
                        'status': instance.status,
                        'created_at': instance.created_at,
                        'image_id': instance.image_id,
                        'vpc_id': instance.vpc_id,
                        'security_group_ids': [sg.security_group_id for sg in instance.security_groups],
                        'zone_id': instance.zone_id,
                        'instance_type_id': instance.instance_type_id,
                        'project_id': instance.project_id
                    }

                    # 应用额外过滤条件
                    if self._match_filters(instance_dict, filters):
                        all_instances.append(instance_dict)

                # 检查是否有更多页
                if len(response.instances) < self.PAGE_SIZE or request.page_number * self.PAGE_SIZE >= total_count:
                    break

                # 获取下一页
                request.page_number += 1

            logger.info(f"查询到符合条件的云主机数量: {len(all_instances)}")
            return all_instances

        except ApiException as e:
            error_msg = f"查询实例失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"查询实例时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def _match_filters(self, instance: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """
        检查实例是否匹配过滤条件

        Args:
            instance: 实例信息
            filters: 过滤条件

        Returns:
            是否匹配
        """
        # 检查安全组ID
        if 'security_group_id' in filters and filters['security_group_id']:
            if filters['security_group_id'] not in instance['security_group_ids']:
                return False

        # 检查VPC ID
        if 'vpc_id' in filters and filters['vpc_id']:
            if instance['vpc_id'] != filters['vpc_id']:
                return False

        # 检查镜像ID
        if 'image_id' in filters and filters['image_id']:
            if instance['image_id'] != filters['image_id']:
                return False

        return True

    def delete_instance(self, instance_id: str) -> Dict[str, Any]:
        """
        删除云主机实例

        Args:
            instance_id: 实例ID

        Returns:
            API响应结果

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始删除云主机，实例ID: {instance_id}")

            # 创建删除请求
            delete_instance_request = volcenginesdkecs.DeleteInstanceRequest(
                instance_id=instance_id,
            )

            # 调用API删除实例
            logger.debug(f"调用DeleteInstance API，请求参数: {delete_instance_request}")
            response = self._retry_api_call(
                self.api_instance.delete_instance,
                delete_instance_request
            )

            logger.info(f"云主机删除成功，实例ID: {instance_id}")
            return {
                'instance_id': instance_id,
                'request_id': response.request_id if hasattr(response, 'request_id') else None
            }

        except ApiException as e:
            error_msg = f"删除实例失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"删除实例时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def batch_delete_instances(self, instance_ids: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        批量删除云主机实例

        Args:
            instance_ids: 实例ID列表

        Returns:
            成功删除的实例列表和失败的实例列表
        """
        success_instances = []
        failed_instances = []

        for instance_id in instance_ids:
            try:
                result = self.delete_instance(instance_id)
                success_instances.append(result)
            except ApiClientError as e:
                failed_instances.append({
                    'instance_id': instance_id,
                    'reason': str(e)
                })

        return success_instances, failed_instances
