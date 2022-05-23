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
from Config.global_dict import set_value
from Config.yaml_read import case_to_object
from Runner.test_runner import parse_api_case_json


@pytest.fixture(scope='session')
def setup():
    project_root = dirname(dirname(abspath(__file__)))
    report_path = os.path.join(project_root, "Report\\allure_raw")
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    parse_api_case_json()
    project_root = dirname(dirname(abspath(__file__)))
    login_api_case_file_path = os.path.join(project_root, 'TestCase\\' + 'login.json')
    api_case = case_to_object(login_api_case_file_path)
    base_request = BaseRequest(api_case.title, api_case.path, api_case.method, api_case.params, api_case.body,
                               api_case.host,
                               api_case.headers)
    response = requests.request(method=base_request.method
                                , url=base_request.host + base_request.path
                                , params=base_request.params
                                , headers=base_request.headers
                                , data=base_request.body)
    assert response.status_code == 200
    set_value('token', response.text)
    if api_case.post_script != '' and api_case.post_script is not None:
        exec(api_case.post_script)
