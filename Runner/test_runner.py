#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:40
# @Author  : martin.peng
# @Site    : 
# @File    : test_runner.py

import importlib

import pytest
import requests

from BaseRequest.base_request import BaseRequest
from Common.read_test_case import parse_api_case_json, init_allure_properties
from Model.api import ApiCase

global_dict = importlib.import_module('Config.global_dict')
set_value = getattr(global_dict, 'set_value')
get_value = getattr(global_dict, 'get_value')

api_case_dict_list = parse_api_case_json()


class TestApiCase:

    @pytest.mark.usefixtures('setup')
    @pytest.mark.parametrize('api_case_params', api_case_dict_list)
    def test_execute_request(self, api_case_params: dict):
        api_case = ApiCase(api_case_params)
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
        if api_case.post_script != '' and api_case.post_script is not None:
            exec(api_case.post_script)
        else:
            assert response.status_code == 200


if __name__ == '__main__':
    pytest.main(['--alluredir', '../Report/allure_raw'])
