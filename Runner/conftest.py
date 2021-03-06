#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/18 14:52
# @Author  : martin.peng
# @Site    : 
# @File    : conftest.py
import os
from os.path import dirname, abspath

import pytest
import requests

from BaseRequest.base_request import BaseRequest
from Config.yaml_read import test_case_to_object
from Runner.test_runner import parse_api_case_yml
from Config.global_dict import set_value


@pytest.fixture()
def setup():
    parse_api_case_yml()
    project_root = dirname(dirname(abspath(__file__)))
    login_api_case_file_path = os.path.join(project_root, 'ApiFile\\' + 'login.yml')
    api_case = test_case_to_object(login_api_case_file_path)
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
