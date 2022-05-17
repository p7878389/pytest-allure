#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:40
# @Author  : martin.peng
# @Site    : 
# @File    : runner.py
import os
from os.path import dirname, abspath

from BaseRequest.base_request import BaseRequest
from Config.global_dict import dict_init
from Config.yaml_read import load_yaml, parse_api_case_file


def runner_init():
    dict_init()
    environ_name = os.environ.get("pytest-allure-environ");
    if environ_name is None or not environ_name.isspace():
        environ_name = 'test'
    project_root = dirname(dirname(abspath(__file__)))
    system_config_file_path = os.path.join(project_root, 'Config\\' + 'config-' + environ_name + '.yml')
    load_yaml(system_config_file_path)


def get_case_file_path_list():
    project_root = dirname(dirname(abspath(__file__)))
    api_case_file_path = os.path.join(project_root, 'ApiFile')
    file_path_list = []
    lookup_file(api_case_file_path, file_path_list)
    return file_path_list


def lookup_file(file_path: str, file_path_list: list):
    files = os.listdir(file_path)
    for file in files:
        current_file_path = os.path.join(file_path, file)
        if os.path.isdir(current_file_path):
            lookup_file(current_file_path, file_path_list)
        if current_file_path.endswith('.yml'):
            file_path_list.append(current_file_path)


if __name__ == '__main__':
    runner_init()
    file_path_list = get_case_file_path_list()
    api_yml_content_list = []
    for api_file_path in file_path_list:
        apiCase = parse_api_case_file(api_file_path)
        BaseRequest(apiCase.title, apiCase.path, apiCase.method, apiCase.params, apiCase.body, apiCase.host,
                    apiCase.headers, apiCase.need_response).execute_request()
