#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
业务操作模块
"""

from typing import Dict, List, Any, Optional
import time
from tqdm import tqdm
from .config import Config
from .api_client import EcsApiClient, ApiClientError


class OperationError(Exception):
    """操作错误异常"""
    pass


class Operations:
    """业务操作类"""

    def __init__(self, config: Config):
        """
        初始化业务操作

        Args:
            config: 配置管理器实例
        """
        self.config = config
        self.credentials = config.get_credentials()

    def list_instances(self, config_group_name: str, sort_by: str = 'created_at',
                      order: str = 'asc', limit: Optional[int] = None) -> Dict[str, Any]:
        """
        查询云主机列表

        Args:
            config_group_name: 配置组名称
            sort_by: 排序字段，默认为created_at
            order: 排序顺序，asc为升序，desc为降序，默认为asc
            limit: 限制显示的实例数量，默认为None（显示所有）

        Returns:
            查询结果统计

        Raises:
            OperationError: 操作失败时抛出
        """
        # 获取配置组
        profile = self.config.get_profile_by_name(config_group_name)
        if not profile:
            raise OperationError(f"未找到配置组: {config_group_name}")

        # 创建API客户端
        api_client = EcsApiClient(
            access_key_id=self.credentials['access_key_id'],
            secret_access_key=self.credentials['secret_access_key'],
            region_id=profile['region_id']
        )

        # 构建查询过滤条件
        filters = {
            'hostname_prefix': profile['hostname_prefix'],
            'security_group_ids': profile.get('security_group_ids'),
            'vpc_id': profile.get('vpc_id'),
            'image_id': profile.get('image_id')
        }

        # 查询符合条件的实例
        try:
            instances = api_client.describe_instances(filters)

            if not instances:
                # 没有找到实例，返回空结果
                return {
                    'total_count': 0,
                    'instances': [],
                    'sort_by': sort_by,
                    'order': order,
                    'limit': limit
                }

            # 按指定字段排序
            reverse = (order == 'desc')

            # 映射排序字段到实际的API返回字段
            sort_field_mapping = {
                'instance_id': 'instance_id',
                'instance_name': 'instance_name',
                'status': 'status',
                'created_at': 'creation_time',  # API可能使用不同的字段名
                'instance_type_id': 'instance_type_id'
            }

            # 获取实际的排序字段
            actual_sort_field = sort_field_mapping.get(sort_by, 'creation_time')

            # 安全地排序，确保字段存在
            try:
                instances.sort(key=lambda x: x.get(actual_sort_field, ''), reverse=reverse)
            except Exception as e:
                # 如果排序出错，尝试使用创建时间排序
                try:
                    instances.sort(key=lambda x: x.get('created_at', ''), reverse=reverse)
                except Exception:
                    # 如果仍然出错，不进行排序
                    pass

            # 限制显示数量
            if limit is not None and limit > 0:
                instances = instances[:limit]

            # 统计结果
            return {
                'total_count': len(instances),
                'instances': instances,
                'sort_by': sort_by,
                'order': order,
                'limit': limit
            }

        except ApiClientError as e:
            raise OperationError(f"查询实例时发生错误: {e}")
        except Exception as e:
            raise OperationError(f"查询实例时发生未知错误: {e}")

    def create_instances(self, config_group_name: str, instance_type: Optional[str], count: int) -> Dict[str, Any]:
        """
        批量创建云主机

        Args:
            config_group_name: 配置组名称
            instance_type: 实例规格，如果为None则使用配置组中的默认值
            count: 创建数量

        Returns:
            创建结果统计

        Raises:
            OperationError: 操作失败时抛出
        """
        # 获取配置组
        profile = self.config.get_profile_by_name(config_group_name)
        if not profile:
            raise OperationError(f"未找到配置组: {config_group_name}")

        # 检查实例规格
        if not instance_type and 'instance_type_id' not in profile:
            raise OperationError(f"未指定实例规格，且配置组'{config_group_name}'中未设置实例规格")

        # 使用配置组中的实例规格或命令行指定的实例规格
        actual_instance_type = instance_type or profile.get('instance_type_id')

        # 创建API客户端
        api_client = EcsApiClient(
            access_key_id=self.credentials['access_key_id'],
            secret_access_key=self.credentials['secret_access_key'],
            region_id=profile['region_id']
        )

        # 准备创建参数
        create_params = {
            'zone_id': profile['zone_id'],
            'image_id': profile['image_id'],
            'instance_type_id': actual_instance_type,
            'security_group_ids': profile['security_group_ids'],
            'vpc_id': profile['vpc_id'],
            'subnet_id': profile['subnet_id'],
            'system_disk_type': profile['system_disk_type'],
            'system_disk_size_gb': profile['system_disk_size_gb'],
            'hostname_prefix': profile['hostname_prefix'],
            'count': count,
            'project_name': profile['project_name'],
            'auto_renew': profile['auto_renew'],
            'auto_renew_period': profile['auto_renew_period'],
            'spot_strategy': profile['spot_strategy']
        }

        # 执行创建操作
        success_instances = []
        failed_instances = []

        # 单次创建的最大实例数量
        MAX_BATCH_SIZE = 100

        # 计算需要创建的批次数
        batch_count = (count + MAX_BATCH_SIZE - 1) // MAX_BATCH_SIZE
        remaining = count

        # 创建进度条
        from .output import Output
        with Output.create_progress_bar(total=count, desc="创建云主机", unit="台") as pbar:
            # 分批创建实例
            for batch in range(batch_count):
                # 计算当前批次需要创建的实例数量
                batch_size = min(MAX_BATCH_SIZE, remaining)

                # 更新当前批次的创建参数
                batch_params = create_params.copy()
                batch_params['count'] = batch_size

                try:
                    # 调用API创建实例
                    result = api_client.create_instances(batch_params)

                    # 记录成功创建的实例
                    for instance_id in result['instance_ids']:
                        success_instances.append({
                            'instance_id': instance_id,
                            'instance_name': result['instance_name']
                        })

                    # 更新进度条
                    pbar.update(len(result['instance_ids']))

                except Exception as e:
                    # 记录创建失败的情况
                    failed_instances.append({
                        'instance_name': f"{profile['hostname_prefix']}-batch{batch+1}",
                        'reason': str(e)
                    })

                    # 更新进度条（失败的也计入进度）
                    pbar.update(batch_size)

                # 更新剩余数量
                remaining -= batch_size

                # 批次之间添加短暂延迟，避免API限流
                if batch < batch_count - 1:
                    time.sleep(1)

        # 统计结果
        success_count = len(success_instances)
        failed_count = count - success_count

        return {
            'success_count': success_count,
            'failed_count': failed_count,
            'total_count': count,
            'success_instances': success_instances,
            'failed_instances': failed_instances
        }

    def delete_instances(self, config_group_name: str, count: int) -> Dict[str, Any]:
        """
        批量销毁云主机

        Args:
            config_group_name: 配置组名称
            count: 销毁数量

        Returns:
            销毁结果统计

        Raises:
            OperationError: 操作失败时抛出
        """
        # 获取配置组
        profile = self.config.get_profile_by_name(config_group_name)
        if not profile:
            raise OperationError(f"未找到配置组: {config_group_name}")

        # 创建API客户端
        api_client = EcsApiClient(
            access_key_id=self.credentials['access_key_id'],
            secret_access_key=self.credentials['secret_access_key'],
            region_id=profile['region_id']
        )

        # 构建查询过滤条件
        filters = {
            'hostname_prefix': profile['hostname_prefix'],
            'security_group_ids': profile.get('security_group_ids'),
            'vpc_id': profile.get('vpc_id'),
            'image_id': profile.get('image_id')
        }

        # 查询符合条件的实例
        try:
            instances = api_client.describe_instances(filters)

            if not instances:
                raise OperationError(f"未找到符合条件的云主机实例，请检查配置组'{config_group_name}'中的筛选条件")

            # 按创建时间从旧到新排序，确保created_at字段存在
            instances.sort(key=lambda x: x.get('created_at', ''))

            # 限制销毁数量
            instances_to_delete = instances[:count]

            if not instances_to_delete:
                raise OperationError(f"没有可销毁的云主机实例")

            # 显示待销毁实例列表并请求确认
            from .output import Output
            if not Output.confirm_delete(instances_to_delete):
                raise OperationError("用户取消了销毁操作")

            # 批量销毁实例
            success_instances = []
            failed_instances = []

            # 单次删除的最大实例数量
            MAX_BATCH_SIZE = 20

            # 计算需要删除的批次数
            total_count = len(instances_to_delete)
            batch_count = (total_count + MAX_BATCH_SIZE - 1) // MAX_BATCH_SIZE

            # 创建进度条
            from .output import Output
            with Output.create_progress_bar(total=total_count, desc="销毁云主机", unit="台") as pbar:
                for i in range(0, total_count, MAX_BATCH_SIZE):
                    # 获取当前批次的实例
                    batch_instances = instances_to_delete[i:i+MAX_BATCH_SIZE]
                    batch_instance_ids = [instance['instance_id'] for instance in batch_instances]

                    # 批量删除实例
                    batch_success, batch_failed = api_client.batch_delete_instances(batch_instance_ids)

                    # 记录成功删除的实例
                    for result in batch_success:
                        # 查找对应的实例信息
                        instance_info = next((instance for instance in batch_instances if instance['instance_id'] == result['instance_id']), None)
                        if instance_info:
                            success_instances.append({
                                'instance_id': result['instance_id'],
                                'instance_name': instance_info['instance_name'],
                                'created_at': instance_info['created_at']
                            })

                    # 记录删除失败的实例
                    for result in batch_failed:
                        # 查找对应的实例信息
                        instance_info = next((instance for instance in batch_instances if instance['instance_id'] == result['instance_id']), None)
                        if instance_info:
                            failed_instances.append({
                                'instance_id': result['instance_id'],
                                'instance_name': instance_info['instance_name'],
                                'created_at': instance_info['created_at'],
                                'reason': result['reason']
                            })

                    # 更新进度条
                    pbar.update(len(batch_instances))

                    # 批次之间添加短暂延迟，避免API限流
                    if i + MAX_BATCH_SIZE < total_count:
                        time.sleep(1)

            # 统计结果
            success_count = len(success_instances)
            failed_count = len(failed_instances)

            return {
                'success_count': success_count,
                'failed_count': failed_count,
                'total_count': total_count,
                'success_instances': success_instances,
                'failed_instances': failed_instances
            }

        except ApiClientError as e:
            raise OperationError(f"查询或销毁实例时发生错误: {e}")
        except Exception as e:
            raise OperationError(f"销毁实例时发生未知错误: {e}")
