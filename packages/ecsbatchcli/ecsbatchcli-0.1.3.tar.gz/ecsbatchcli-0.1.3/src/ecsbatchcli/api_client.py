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
import volcenginesdkvpc
from volcenginesdkcore.rest import ApiException

from .rate_limiter import vpc_api_rate_limiter

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
                # 应用速率限制
                vpc_api_rate_limiter.acquire()
                return func(*args, **kwargs)
            except ApiException as e:
                last_exception = e
                # 解析错误信息
                error_code = getattr(e, 'status', None)
                error_message = str(e)

                # 尝试解析响应体
                try:
                    import json
                    response_body = json.loads(e.body)
                    error_detail = response_body.get('Error', {})
                    error_code_api = error_detail.get('Code', 'Unknown')
                    error_msg_api = error_detail.get('Message', 'No message')

                    # 记录详细错误信息
                    logger.warning(f"API调用失败 (尝试 {attempt}/{self.MAX_RETRIES}): 错误码={error_code}, API错误码={error_code_api}, API错误信息={error_msg_api}")
                    print(f"完整错误响应: {json.dumps(response_body, indent=2)}")
                except Exception as parse_error:
                    # 如果解析失败，记录原始错误信息
                    logger.warning(f"API调用失败 (尝试 {attempt}/{self.MAX_RETRIES}): 错误码={error_code}, 错误信息={error_message}")
                    print(f"无法解析错误响应: {e.body}")
                    print(f"解析错误: {parse_error}")

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
                - zone_id: 可用区ID
                - image_id: 镜像ID
                - instance_type_id: 实例规格
                - security_group_ids: 安全组ID列表
                - subnet_id: 子网ID
                - vpc_id: VPC ID
                - system_disk_type: 系统盘类型
                - system_disk_size_gb: 系统盘大小（GB）
                - hostname_prefix: 主机名前缀
                - count: 创建数量
                - project_name: 项目名称
                - auto_renew: 是否自动续费
                - auto_renew_period: 续费时长
                - spot_strategy: 抢占式实例策略

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
                security_group_ids=params['security_group_ids'],
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
                instance_type_id=params['instance_type_id'],
                # 保留镜像登录凭证
                keep_image_credential=True,
                # 网络接口
                network_interfaces=[req_network_interfaces],
                # 系统盘
                volumes=[req_volumes],
                # 可用区ID
                zone_id=params['zone_id'],
                # 项目名称
                project_name=params['project_name'],
                # 竞价策略
                spot_strategy=params['spot_strategy'],
                # 自动续费
                auto_renew=params['auto_renew'],
                # 续费时长
                auto_renew_period=params['auto_renew_period'],
            )

            # 调用API创建实例
            logger.debug(f"调用RunInstances API，请求参数: {run_instances_request}")
            response = self._retry_api_call(
                self.api_instance.run_instances,
                run_instances_request
            )

            logger.info(f"云主机创建成功，实例ID: {response.instance_ids}")
            result = {
                'instance_ids': response.instance_ids,
                'instance_name': instance_name
            }

            # 检查request_id属性是否存在
            if hasattr(response, 'request_id'):
                result['request_id'] = response.request_id

            return result

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
            request = volcenginesdkecs.DescribeInstancesRequest()

            # 设置分页参数
            # 注意：根据火山引擎SDK的API，可能需要使用属性设置而不是构造函数参数
            request.max_results = self.PAGE_SIZE
            request.next_token = ""  # 初始为空字符串，表示从第一页开始

            # 添加过滤条件
            # 创建过滤器列表
            filters_list = []

            if 'hostname_prefix' in filters and filters['hostname_prefix']:
                # 使用实例名称前缀过滤
                # 注意：根据火山引擎SDK的API，可能需要使用不同的过滤方式
                filters_list.append({
                    'name': 'instance-name',
                    'values': [f"{filters['hostname_prefix']}*"]
                })

            if 'instance_ids' in filters and filters['instance_ids']:
                # 使用实例ID列表过滤
                filters_list.append({
                    'name': 'instance-id',
                    'values': filters['instance_ids']
                })

            if 'security_group_ids' in filters and filters['security_group_ids']:
                # 使用安全组ID过滤
                filters_list.append({
                    'name': 'security-group-id',
                    'values': filters['security_group_ids']
                })

            if 'vpc_id' in filters and filters['vpc_id']:
                # 使用VPC ID过滤
                filters_list.append({
                    'name': 'vpc-id',
                    'values': [filters['vpc_id']]
                })

            if 'image_id' in filters and filters['image_id']:
                # 使用镜像ID过滤
                filters_list.append({
                    'name': 'image-id',
                    'values': [filters['image_id']]
                })

            # 设置过滤器
            if filters_list:
                request.filters = filters_list

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
                    # 转换为字典格式，安全地获取所有属性
                    instance_dict = {
                        'instance_id': getattr(instance, 'instance_id', ''),
                        'instance_name': getattr(instance, 'instance_name', ''),
                        'status': getattr(instance, 'status', ''),
                        'created_at': getattr(instance, 'created_at', ''),
                        'image_id': getattr(instance, 'image_id', ''),
                        'vpc_id': getattr(instance, 'vpc_id', ''),
                        'zone_id': getattr(instance, 'zone_id', ''),
                        'instance_type_id': getattr(instance, 'instance_type_id', ''),
                        'project_id': getattr(instance, 'project_id', '')
                    }

                    # 安全地获取安全组IDs
                    if hasattr(instance, 'security_groups') and instance.security_groups:
                        try:
                            # 尝试获取security_group_id属性
                            instance_dict['security_group_ids'] = [
                                getattr(sg, 'security_group_id', '')
                                for sg in instance.security_groups
                                if hasattr(sg, 'security_group_id')
                            ]
                        except Exception as e:
                            logger.warning(f"获取安全组ID时出错: {e}")
                            instance_dict['security_group_ids'] = []
                    else:
                        # 如果没有security_groups属性或为空，设置为空列表
                        instance_dict['security_group_ids'] = []

                    # 应用额外过滤条件
                    if self._match_filters(instance_dict, filters):
                        all_instances.append(instance_dict)

                # 检查是否有更多页
                if not response.next_token or len(response.instances) < self.PAGE_SIZE:
                    break

                # 获取下一页
                request.next_token = response.next_token

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

        注意：大部分过滤条件已经在API请求中处理，这里只做额外的检查

        Args:
            instance: 实例信息
            filters: 过滤条件

        Returns:
            是否匹配
        """
        # 由于我们已经在API请求中添加了大部分过滤条件，这里只需要做一些额外的检查
        # 例如，检查主机名是否以指定前缀开头（如果API不支持前缀过滤）
        if 'hostname_prefix' in filters and filters['hostname_prefix']:
            if not instance.get('instance_name', '').startswith(filters['hostname_prefix']):
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


class VpcApiClient:
    """火山引擎VPC API客户端"""

    # 最大重试次数
    MAX_RETRIES = 3
    # 重试间隔（秒）
    RETRY_INTERVAL = 2
    # 每页查询数量
    PAGE_SIZE = 50

    def __init__(self, access_key_id: str, secret_access_key: str, region_id: str):
        """
        初始化VPC API客户端

        Args:
            access_key_id: 访问密钥ID
            secret_access_key: 访问密钥
            region_id: 区域ID
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_id = region_id
        self.api_instance = self._init_api_instance()
        logger.debug(f"初始化VpcApiClient，区域: {region_id}")

    def _init_api_instance(self) -> volcenginesdkvpc.VPCApi:
        """
        初始化API实例

        Returns:
            VPC API实例
        """
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = self.access_key_id
        configuration.sk = self.secret_access_key
        configuration.region = self.region_id
        volcenginesdkcore.Configuration.set_default(configuration)

        return volcenginesdkvpc.VPCApi()



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
        # 应用速率限制
        vpc_api_rate_limiter.acquire()
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

                # 尝试解析响应体
                try:
                    import json
                    response_body = json.loads(e.body)
                    error_detail = response_body.get('Error', {})
                    error_code_api = error_detail.get('Code', 'Unknown')
                    error_msg_api = error_detail.get('Message', 'No message')

                    # 记录详细错误信息
                    logger.warning(f"API调用失败 (尝试 {attempt}/{self.MAX_RETRIES}): 错误码={error_code}, API错误码={error_code_api}, API错误信息={error_msg_api}")
                except Exception as parse_error:
                    # 如果解析失败，记录原始错误信息
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

    def describe_network_interfaces(self, status='Available', type='secondary', page_size=100, page_number=1) -> Dict[str, Any]:
        """
        查询网卡（单页）

        Args:
            status: 网卡状态，默认为'Available'（未挂载）
            type: 网卡类型，默认为'secondary'（辅助网卡）
            page_size: 每页记录数，默认为100
            page_number: 页码，默认为1

        Returns:
            查询结果，包含网卡列表

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始查询网卡，状态: {status}, 类型: {type}, 页码: {page_number}, 每页数量: {page_size}")

            # 构建查询请求
            request = volcenginesdkvpc.DescribeNetworkInterfacesRequest(
                status=status,
                type=type,
                page_size=page_size,
                page_number=page_number
            )

            # 调用API查询网卡
            logger.debug(f"调用DescribeNetworkInterfaces API，请求参数: {request}")
            response = self._retry_api_call(
                self.api_instance.describe_network_interfaces,
                request
            )

            logger.info(f"查询网卡成功，数量: {len(response.network_interface_sets) if hasattr(response, 'network_interface_sets') else 0}")
            return response

        except ApiException as e:
            error_msg = f"查询网卡失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"查询网卡时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def describe_all_network_interfaces(self, status='Available', type='secondary', page_size=100) -> List[Any]:
        """
        查询所有网卡（分页查询）

        Args:
            status: 网卡状态，默认为'Available'（未挂载）
            type: 网卡类型，默认为'secondary'（辅助网卡）
            page_size: 每页记录数，默认为100

        Returns:
            所有网卡列表

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始分页查询所有网卡，状态: {status}, 类型: {type}")

            all_network_interfaces = []
            page_number = 1
            total_count = 0

            # 创建进度条
            from .output import Output
            with Output.create_progress_bar(total=None, desc="查询网卡", unit="页") as pbar:
                while True:
                    # 查询当前页
                    response = self.describe_network_interfaces(
                        status=status,
                        type=type,
                        page_size=page_size,
                        page_number=page_number
                    )

                    # 获取当前页的网卡列表
                    current_page_interfaces = []
                    if hasattr(response, 'network_interface_sets') and response.network_interface_sets:
                        current_page_interfaces = response.network_interface_sets

                    # 添加到总列表
                    all_network_interfaces.extend(current_page_interfaces)

                    # 获取总数
                    if hasattr(response, 'total_count'):
                        total_count = response.total_count
                        # 更新进度条总数
                        if pbar.total is None:
                            pbar.total = (total_count + page_size - 1) // page_size  # 向上取整

                    # 更新进度条
                    pbar.update(1)

                    # 判断是否还有下一页
                    current_page_count = len(current_page_interfaces)
                    if current_page_count < page_size:
                        # 当前页不满，说明已经是最后一页
                        break

                    # 获取下一页
                    page_number += 1

                    # 添加短暂延迟，避免API限流
                    time.sleep(0.5)

            logger.info(f"分页查询网卡完成，总数量: {len(all_network_interfaces)}")
            return all_network_interfaces

        except ApiException as e:
            error_msg = f"分页查询网卡失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"分页查询网卡时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def delete_network_interface(self, network_interface_id: str) -> Dict[str, Any]:
        """
        删除网卡

        Args:
            network_interface_id: 网卡ID

        Returns:
            删除结果

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始删除网卡，ID: {network_interface_id}")

            # 构建删除请求
            request = volcenginesdkvpc.DeleteNetworkInterfaceRequest(
                network_interface_id=network_interface_id
            )

            # 调用API删除网卡
            logger.debug(f"调用DeleteNetworkInterface API，请求参数: {request}")
            response = self._retry_api_call(
                self.api_instance.delete_network_interface,
                request
            )

            logger.info(f"删除网卡成功，ID: {network_interface_id}")
            return {
                'network_interface_id': network_interface_id,
                'request_id': response.request_id if hasattr(response, 'request_id') else None
            }

        except ApiException as e:
            error_msg = f"删除网卡失败: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)
        except Exception as e:
            error_msg = f"删除网卡时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def batch_delete_network_interfaces(self, network_interfaces: List[Any], max_workers: int = 10) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        批量删除网卡（并发）

        Args:
            network_interfaces: 网卡列表
            max_workers: 最大并发数，默认为10

        Returns:
            成功删除的网卡列表和失败的网卡列表

        Raises:
            ApiClientError: API调用失败时抛出
        """
        try:
            logger.info(f"开始批量删除网卡，数量: {len(network_interfaces)}, 最大并发数: {max_workers}")

            # 导入并发库
            import concurrent.futures
            from .output import Output

            # 创建线程池
            success_interfaces = []
            failed_interfaces = []

            # 创建进度条
            with Output.create_progress_bar(total=len(network_interfaces), desc="删除网卡", unit="个") as pbar:
                # 使用线程池并发删除
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # 提交所有任务
                    future_to_interface = {
                        executor.submit(self._delete_network_interface_task, interface.network_interface_id): interface
                        for interface in network_interfaces
                    }

                    # 处理完成的任务
                    for future in concurrent.futures.as_completed(future_to_interface):
                        interface = future_to_interface[future]
                        try:
                            # 获取任务结果
                            result = future.result()

                            # 记录成功删除的网卡
                            success_interfaces.append({
                                'network_interface_id': interface.network_interface_id,
                                'vpc_id': getattr(interface, 'vpc_id', ''),
                                'subnet_id': getattr(interface, 'subnet_id', ''),
                                'zone_id': getattr(interface, 'zone_id', ''),
                                'mac_address': getattr(interface, 'mac_address', ''),
                                'status': getattr(interface, 'status', '')
                            })
                        except Exception as e:
                            # 记录删除失败的网卡
                            failed_interfaces.append({
                                'network_interface_id': interface.network_interface_id,
                                'vpc_id': getattr(interface, 'vpc_id', ''),
                                'subnet_id': getattr(interface, 'subnet_id', ''),
                                'zone_id': getattr(interface, 'zone_id', ''),
                                'mac_address': getattr(interface, 'mac_address', ''),
                                'status': getattr(interface, 'status', ''),
                                'reason': str(e)
                            })
                        finally:
                            # 更新进度条
                            pbar.update(1)

            logger.info(f"批量删除网卡完成，成功: {len(success_interfaces)}, 失败: {len(failed_interfaces)}")
            return success_interfaces, failed_interfaces

        except Exception as e:
            error_msg = f"批量删除网卡时发生未知错误: {e}"
            logger.error(error_msg)
            raise ApiClientError(error_msg)

    def _delete_network_interface_task(self, network_interface_id: str) -> Dict[str, Any]:
        """
        删除网卡任务（供线程池使用）

        Args:
            network_interface_id: 网卡ID

        Returns:
            删除结果

        Raises:
            Exception: 删除失败时抛出
        """
        try:
            # 删除网卡
            result = self.delete_network_interface(network_interface_id)
            return result
        except Exception as e:
            # 记录错误并重新抛出
            logger.warning(f"删除网卡任务失败，ID: {network_interface_id}, 错误: {e}")
            raise
