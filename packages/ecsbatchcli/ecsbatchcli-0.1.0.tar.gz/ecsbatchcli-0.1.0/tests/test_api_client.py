#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API客户端模块测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 创建模拟模块
class MockApiException(Exception):
    pass

# 创建模拟的volcenginesdkcore模块
mock_volcenginesdkcore = MagicMock()
mock_volcenginesdkcore.Configuration = MagicMock()
mock_volcenginesdkcore.rest = MagicMock()
mock_volcenginesdkcore.rest.ApiException = MockApiException

# 创建模拟的volcenginesdkecs模块
mock_volcenginesdkecs = MagicMock()
mock_volcenginesdkecs.ECSApi = MagicMock()
mock_volcenginesdkecs.NetworkInterfaceForRunInstancesInput = MagicMock()
mock_volcenginesdkecs.VolumeForRunInstancesInput = MagicMock()
mock_volcenginesdkecs.RunInstancesRequest = MagicMock()
mock_volcenginesdkecs.DescribeInstancesRequest = MagicMock()
mock_volcenginesdkecs.DeleteInstanceRequest = MagicMock()

# 注册模拟模块
sys.modules['volcenginesdkcore'] = mock_volcenginesdkcore
sys.modules['volcenginesdkecs'] = mock_volcenginesdkecs
sys.modules['volcenginesdkcore.rest'] = mock_volcenginesdkcore.rest

# 导入被测试的模块
with patch('src.ecsbatchcli.api_client.volcenginesdkcore', mock_volcenginesdkcore):
    with patch('src.ecsbatchcli.api_client.volcenginesdkecs', mock_volcenginesdkecs):
        with patch('src.ecsbatchcli.api_client.ApiException', MockApiException):
            from src.ecsbatchcli.api_client import EcsApiClient, ApiClientError


class TestEcsApiClient(unittest.TestCase):
    """API客户端测试类"""

    def setUp(self):
        """测试前准备"""
        # 模拟API实例
        self.mock_api_instance = MagicMock()

        # 创建API客户端
        with patch('src.ecsbatchcli.api_client.volcenginesdkecs.ECSApi', return_value=self.mock_api_instance):
            self.api_client = EcsApiClient(
                access_key_id='test_key',
                secret_access_key='test_secret',
                region_id='cn-beijing'
            )

    def test_init_api_instance(self):
        """测试初始化API实例"""
        with patch('src.ecsbatchcli.api_client.volcenginesdkcore.Configuration') as mock_config:
            with patch('src.ecsbatchcli.api_client.volcenginesdkecs.ECSApi') as mock_ecs_api:
                api_client = EcsApiClient(
                    access_key_id='test_key',
                    secret_access_key='test_secret',
                    region_id='cn-beijing'
                )

                # 验证Configuration设置
                mock_config.assert_called_once()
                mock_config_instance = mock_config.return_value
                self.assertEqual(mock_config_instance.ak, 'test_key')
                self.assertEqual(mock_config_instance.sk, 'test_secret')
                self.assertEqual(mock_config_instance.region, 'cn-beijing')

                # 验证ECSApi创建
                mock_ecs_api.assert_called_once()

    def test_retry_api_call_success(self):
        """测试API调用重试机制（成功）"""
        # 模拟成功的API调用
        mock_func = MagicMock(return_value='success')

        # 调用重试函数
        result = self.api_client._retry_api_call(mock_func, 'arg1', 'arg2', kwarg1='value1')

        # 验证结果
        self.assertEqual(result, 'success')
        mock_func.assert_called_once_with('arg1', 'arg2', kwarg1='value1')

    def test_retry_api_call_failure(self):
        """测试API调用重试机制（失败）"""
        # 模拟失败的API调用
        mock_func = MagicMock(side_effect=MockApiException('API error'))

        # 调用重试函数，应该抛出异常
        with self.assertRaises(ApiClientError):
            self.api_client._retry_api_call(mock_func)

        # 验证调用次数
        self.assertEqual(mock_func.call_count, self.api_client.MAX_RETRIES)

    def test_create_instances(self):
        """测试创建云主机实例"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.instance_ids = ['i-test1', 'i-test2']
        mock_response.request_id = 'req-test'
        self.mock_api_instance.run_instances.return_value = mock_response

        # 创建实例参数
        params = {
            'availability_zone_id': 'cn-beijing-a',
            'image_id': 'image-test',
            'instance_type': 'ecs.g1ie.large',
            'security_group_id': 'sg-test',
            'subnet_id': 'subnet-test',
            'vpc_id': 'vpc-test',
            'system_disk_type': 'ESSD_PL0',
            'system_disk_size_gb': 40,
            'hostname_prefix': 'test-server',
            'count': 2,
            'project_id': 'project-test'
        }

        # 调用创建实例方法
        with patch('src.ecsbatchcli.api_client.datetime') as mock_datetime:
            # 模拟当前时间
            mock_now = MagicMock()
            mock_now.strftime.return_value = '0101010101'
            mock_datetime.now.return_value = mock_now

            result = self.api_client.create_instances(params)

        # 验证结果
        self.assertEqual(result['instance_ids'], ['i-test1', 'i-test2'])
        self.assertEqual(result['instance_name'], 'test-server-0101010101')
        self.assertEqual(result['request_id'], 'req-test')

        # 验证API调用
        self.mock_api_instance.run_instances.assert_called_once()

        # 由于我们使用的是MagicMock，无法直接验证参数值，只能验证调用次数
        self.assertEqual(self.mock_api_instance.run_instances.call_count, 1)

    def test_describe_instances(self):
        """测试查询云主机实例"""
        # 模拟API响应
        mock_instance1 = MagicMock()
        mock_instance1.instance_id = 'i-test1'
        mock_instance1.instance_name = 'test-server-001'
        mock_instance1.status = 'RUNNING'
        mock_instance1.created_at = '2023-01-01T00:00:00Z'
        mock_instance1.image_id = 'image-test'
        mock_instance1.vpc_id = 'vpc-test'
        mock_instance1.security_groups = [MagicMock(security_group_id='sg-test')]
        mock_instance1.zone_id = 'cn-beijing-a'
        mock_instance1.instance_type_id = 'ecs.g1ie.large'
        mock_instance1.project_id = 'project-test'

        mock_instance2 = MagicMock()
        mock_instance2.instance_id = 'i-test2'
        mock_instance2.instance_name = 'test-server-002'
        mock_instance2.status = 'RUNNING'
        mock_instance2.created_at = '2023-01-02T00:00:00Z'
        mock_instance2.image_id = 'image-test'
        mock_instance2.vpc_id = 'vpc-test'
        mock_instance2.security_groups = [MagicMock(security_group_id='sg-test')]
        mock_instance2.zone_id = 'cn-beijing-a'
        mock_instance2.instance_type_id = 'ecs.g1ie.large'
        mock_instance2.project_id = 'project-test'

        mock_response = MagicMock()
        mock_response.instances = [mock_instance1, mock_instance2]
        mock_response.total_count = 2
        self.mock_api_instance.describe_instances.return_value = mock_response

        # 查询过滤条件
        filters = {
            'hostname_prefix': 'test-server',
            'security_group_id': 'sg-test',
            'vpc_id': 'vpc-test',
            'image_id': 'image-test'
        }

        # 调用查询实例方法
        result = self.api_client.describe_instances(filters)

        # 验证结果
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['instance_id'], 'i-test1')
        self.assertEqual(result[0]['instance_name'], 'test-server-001')
        self.assertEqual(result[1]['instance_id'], 'i-test2')
        self.assertEqual(result[1]['instance_name'], 'test-server-002')

        # 验证API调用
        self.mock_api_instance.describe_instances.assert_called_once()
        call_args = self.mock_api_instance.describe_instances.call_args[0][0]
        self.assertEqual(call_args.instance_name_prefix, 'test-server')

    def test_delete_instance(self):
        """测试删除云主机实例"""
        # 模拟API响应
        mock_response = MagicMock()
        mock_response.request_id = 'req-test'
        self.mock_api_instance.delete_instance.return_value = mock_response

        # 调用删除实例方法
        result = self.api_client.delete_instance('i-test1')

        # 验证结果
        self.assertEqual(result['instance_id'], 'i-test1')
        self.assertEqual(result['request_id'], 'req-test')

        # 验证API调用
        self.mock_api_instance.delete_instance.assert_called_once()

    def test_batch_delete_instances(self):
        """测试批量删除云主机实例"""
        # 重置mock对象
        self.mock_api_instance.delete_instance.reset_mock()

        # 模拟API响应
        mock_response = MagicMock()
        mock_response.request_id = 'req-test'

        # 模拟第二个实例删除失败
        def side_effect(request):
            if hasattr(request, 'instance_id') and request.instance_id == 'i-test2':
                raise MockApiException('API error')
            return mock_response

        self.mock_api_instance.delete_instance.side_effect = side_effect

        # 使用patch替换delete_instance方法，以便我们可以模拟它的行为
        with patch.object(self.api_client, 'delete_instance') as mock_delete:
            # 设置mock_delete的行为
            def delete_side_effect(instance_id):
                if instance_id == 'i-test2':
                    raise ApiClientError('API error')
                return {'instance_id': instance_id, 'request_id': 'req-test'}

            mock_delete.side_effect = delete_side_effect

            # 调用批量删除实例方法
            success, failed = self.api_client.batch_delete_instances(['i-test1', 'i-test2', 'i-test3'])

        # 验证结果
        self.assertEqual(len(success), 2)
        self.assertEqual(success[0]['instance_id'], 'i-test1')
        self.assertEqual(success[1]['instance_id'], 'i-test3')

        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]['instance_id'], 'i-test2')
        self.assertIn('API error', failed[0]['reason'])

        # 验证API调用次数
        self.assertEqual(mock_delete.call_count, 3)


if __name__ == '__main__':
    unittest.main()
