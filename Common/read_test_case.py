#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 16:49
# @Author  : martin.peng
# @Site    : 
# @File    : read_test_case.py


import os
from os.path import dirname, abspath
from typing import List

import allure

from Config.yaml_read import parse_system_yaml, case_to_object
from Model.api import ApiCase


def load_system_yaml():
    environ_name = os.environ.get("pytest-allure-environ");
    if environ_name is None or not environ_name.isspace():
        environ_name = 'test'
    project_root = dirname(dirname(abspath(__file__)))
    system_config_file_path = os.path.join(project_root, 'Config\\' + 'config-' + environ_name + '.yml')
    parse_system_yaml(system_config_file_path)


def get_case_file_path_list():
    project_root = dirname(dirname(abspath(__file__)))
    api_case_file_path = os.path.join(project_root, 'TestCase')
    file_path_list = []
    lookup_api_case_file(api_case_file_path, file_path_list)
    return file_path_list


def lookup_api_case_file(file_path: str, file_path_list: list):
    files = os.listdir(file_path)
    for file in files:
        current_file_path = os.path.join(file_path, file)
        if os.path.isdir(current_file_path):
            lookup_api_case_file(current_file_path, file_path_list)
        if current_file_path.endswith('.json'):
            file_path_list.append(current_file_path)


def parse_api_case_json() -> List[dict]:
    """

    :rtype: List[dict] = []
    """
    load_system_yaml()
    api_case_dict = {}
    file_path_list = get_case_file_path_list()
    for api_file_path in file_path_list:
        api_case = case_to_object(api_file_path)
        if api_case.skip:
            continue
        api_case_dict[api_case.title] = api_case
    return sort_api_case(api_case_dict)


def sort_api_case(_api_case_dict: dict) -> List[dict]:
    """

    :rtype: List[dict]
    """
    sort_list = []
    api_case_dict_list: List[dict] = []
    for key in list(_api_case_dict.keys()):
        item = _api_case_dict.get(key)
        if item.dependency == '':
            sort_list.append(item)
            _api_case_dict.pop(key)
            _sort_api_case(_api_case_dict, sort_list, item)
    for api_case_item in sort_list:
        api_case_dict_list.append(api_case_item.__dict__)
    return api_case_dict_list


def _sort_api_case(_api_case_dict, dependency_list, item: ApiCase):
    for key in list(_api_case_dict.keys()):
        dependency_item = _api_case_dict.get(key)
        dependency = dependency_item.dependency
        if dependency == '' or dependency != item.title:
            continue
        _api_case_dict.pop(key)
        dependency_list.append(dependency_item)
        _sort_api_case(_api_case_dict, dependency_list, dependency_item)


def init_allure_properties(api_case: ApiCase):
    allure.dynamic.title(api_case.title)
    allure.dynamic.story(api_case.story)
    allure.dynamic.description(api_case.description)
    allure.dynamic.feature(api_case.feature)
