#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:40
# @Author  : martin.peng
# @Site    : 
# @File    : test_runner.py
import os
from os.path import dirname, abspath

import allure
import pytest
import requests

from BaseRequest.base_request import BaseRequest
from Config.global_dict import dict_init,set_value
from Config.yaml_read import parse_system_yaml, test_case_to_object
from Model.api import ApiCase

api_case_list = []
ids = []


def load_system_yaml():
    dict_init()
    environ_name = os.environ.get("pytest-allure-environ");
    if environ_name is None or not environ_name.isspace():
        environ_name = 'test'
    project_root = dirname(dirname(abspath(__file__)))
    system_config_file_path = os.path.join(project_root, 'Config\\' + 'config-' + environ_name + '.yml')
    parse_system_yaml(system_config_file_path)


def get_case_file_path_list():
    project_root = dirname(dirname(abspath(__file__)))
    api_case_file_path = os.path.join(project_root, 'ApiFile')
    file_path_list = []
    lookup_api_case_file(api_case_file_path, file_path_list)
    return file_path_list


def lookup_api_case_file(file_path: str, file_path_list: list):
    files = os.listdir(file_path)
    for file in files:
        current_file_path = os.path.join(file_path, file)
        if os.path.isdir(current_file_path):
            lookup_api_case_file(current_file_path, file_path_list)
        if current_file_path.endswith('.yml'):
            file_path_list.append(current_file_path)


def parse_api_case_yml():
    load_system_yaml()
    file_path_list = get_case_file_path_list()
    global ids
    for api_file_path in file_path_list:
        api_case = test_case_to_object(api_file_path)
        if api_case.skip:
            continue
        api_case_list.append(api_case.__dict__)


def _init_allure_properties(api_case: ApiCase):
    allure.dynamic.title(api_case.title)
    allure.dynamic.story(api_case.story)
    allure.dynamic.description(api_case.description)
    allure.dynamic.feature(api_case.feature)


parse_api_case_yml()


class TestApiCase:

    @pytest.mark.usefixtures('setup')
    @pytest.mark.parametrize('api_case_params', api_case_list)
    def test_execute_request(self, api_case_params: dict):
        api_case = ApiCase(api_case_params)
        _init_allure_properties(api_case)
        base_request = BaseRequest(api_case.title, api_case.path, api_case.method, api_case.params, api_case.body,
                                   api_case.host,
                                   api_case.headers)
        response = requests.request(method=base_request.method
                                    , url=base_request.host + base_request.path
                                    , params=base_request.params
                                    , headers=base_request.headers
                                    , data=base_request.body)
        assert response.status_code == 200
        if api_case.response_script != '' and api_case.response_script is not None:
            exec(api_case.response_script)
