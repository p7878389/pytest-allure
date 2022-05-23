#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 9:05
# @Author  : martin.peng
# @Site    : 
# @File    : test_case.py
import os
from os.path import dirname, abspath

import pytest
import requests

from BaseRequest.base_request import BaseRequest
from Config.yaml_read import case_to_object
from Runner.test_runner import init_allure_properties
from Common.read_test_case import load_system_yaml

test_case_file_name = 'Admin/clover_api_key.json'


class TestCase:
    load_system_yaml()

    @pytest.mark.usefixtures('setup')
    def test_execute_request(self):
        project_root = dirname(dirname(abspath(__file__)))
        api_case_file_path = os.path.join(project_root, 'TestCase')
        api_case_file_path += '\\' + test_case_file_name
        api_case = case_to_object(api_case_file_path)
        init_allure_properties(api_case)
        if api_case.pre_script != '':
            exec(api_case.pre_script)
        base_request = BaseRequest(api_case.title, api_case.path, api_case.method, api_case.params, api_case.body,
                                   api_case.host,
                                   api_case.headers)
        response = requests.request(method=base_request.method
                                    , url=base_request.host + base_request.path
                                    , params=base_request.params
                                    , headers=base_request.headers
                                    , data=base_request.body)
        # assert response.status_code == 200
        if api_case.post_script != '' and api_case.post_script is not None:
            exec(api_case.post_script)
