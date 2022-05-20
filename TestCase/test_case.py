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

from Config.yaml_read import test_case_to_object
from BaseRequest.base_request import BaseRequest
from Runner.test_runner import init_allure_properties
from Runner.test_runner import load_system_yaml
from Runner.conftest import setup

test_case_file_name = 'get_auth_id.json'


class TestCase:
    load_system_yaml()

    @pytest.mark.usefixtures('setup')
    def test_execute_request(self):
        project_root = dirname(dirname(abspath(__file__)))
        api_case_file_path = os.path.join(project_root, 'TestCase')
        api_case_file_path += '\\' + test_case_file_name
        api_case = test_case_to_object(api_case_file_path)
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
