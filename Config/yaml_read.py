#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 9:31
# @Author  : martin.peng
# @Site    : 
# @File    : yaml_read.py
import json
import os
import string

import yaml

from Config.global_dict import set_value, set_file_path_config, get_api_server_config, set_logging_config, \
    set_api_server_config
from Model.api import ApiServerConfig, FileDataConfig, ApiCase, LoggingConfig, TestCaseData, TestCase


def parse_yaml_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    content = yaml.load(file_content, Loader=yaml.FullLoader)
    yaml_dict = {}
    yaml_dict.update(content)
    return yaml_dict


def parse_json_to_dict(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    content = json.loads(file_content)
    json_dict = {}
    json_dict.update(content)
    return json_dict


def parse_system_yaml(file_path: string):
    yaml_dict = parse_yaml_to_dict(file_path)
    api_server_config = ApiServerConfig(yaml_dict['api-server'])
    if api_server_config.api_key is None or api_server_config.api_key == '':
        api_server_config.api_key = os.environ.get('WPS_API_KEY')

    if api_server_config.secret is None or api_server_config.secret == '':
        api_server_config.secret = os.environ.get('WPS_SECRET')

    if api_server_config.host is None or api_server_config.host == '':
        api_server_config.host = os.environ.get('WPS_HOST')

    set_api_server_config(api_server_config)
    set_file_path_config(FileDataConfig(yaml_dict['file_path']))
    set_logging_config(LoggingConfig(yaml_dict['logging']))
    set_value(file_path, yaml_dict)


def case_to_object(file_path: str) -> ApiCase:
    content = parse_json_to_dict(file_path)
    content['host'] = get_api_server_config().host
    content.setdefault('body', None)
    content.setdefault('headers', {})
    content.setdefault('need_response', False)
    content.setdefault('post_script', '')
    content.setdefault('skip', False)
    content.setdefault('params', {})
    content.setdefault('dependency', '')
    content.setdefault('pre_script', '')
    return ApiCase(content)


def parse_test_data_to_object(file_path: str) -> TestCase:
    test_case_data_list = []
    content = parse_json_to_dict(file_path)
    content_data_dict = content.get('data', None)
    # if isinstance(None, content_data_dict):
    #     content['data'] = []
    #     return TestCase(content)
    if isinstance(content_data_dict, list):
        for _content_data_dict in content_data_dict:
            set_attributes(_content_data_dict)
            test_case_data_list.append(TestCaseData(_content_data_dict))
    content['data'] = test_case_data_list
    return TestCase(content)


def set_attributes(content: dict):
    content.setdefault('body', None)
    content.setdefault('headers', {})
    content.setdefault('post_script', '')
    content.setdefault('params', {})
    content.setdefault('pre_script', '')
