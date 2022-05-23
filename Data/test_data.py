#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 16:31
# @Author  : martin.peng
# @Site    : 
# @File    : test_data.py
import importlib

import pytest
import requests

from BaseRequest.base_request import BaseRequest
from Common.read_test_case import read_test_case_data, init_allure_properties
from Model.api import ApiCase
from Runner.test_runner import parse_api_case_json

global_dict = importlib.import_module('Config.global_dict')
set_value = getattr(global_dict, 'set_value')
get_value = getattr(global_dict, 'get_value')

api_case_data_params = []
new_api_case_dict = {}
test_case_data_dict = {}

api_case_dict_list = parse_api_case_json()
test_case_data_list = read_test_case_data()
for case_item in test_case_data_list:
    test_case_data_dict.setdefault(case_item.title, case_item)
for item in api_case_dict_list:
    case_item = test_case_data_dict.get(item.get('title'), None)
    if case_item is None:
        continue
    for case_data_item in case_item.data:
        __dict__ = dict(item)
        __dict__['path'] = case_data_item.path
        __dict__['params'] = case_data_item.params
        __dict__['headers'] = case_data_item.headers
        __dict__['body'] = case_data_item.body
        __dict__['post_script'] = case_data_item.post_script
        __dict__['pre_script'] = case_data_item.pre_script
        api_case_data_params.append(
            (item['title'] + '_' + case_data_item.id, __dict__.get('path'), __dict__.get('headers'),
             __dict__.get('params'),
             __dict__.get('body')))
        new_api_case_dict[item['title'] + '_' + case_data_item.id] = __dict__


class TestApiCase:

    @pytest.mark.usefixtures('setup')
    @pytest.mark.parametrize('title, path, headers, params, body', api_case_data_params)
    def test_execute_request(self, title, path, headers, params, body):
        api_case = ApiCase(new_api_case_dict[title])
        init_allure_properties(api_case)
        if api_case.pre_script != '':
            exec(api_case.pre_script)
        base_request = BaseRequest(api_case.title, path, api_case.method, params, body,
                                   api_case.host,
                                   headers)
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
