#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 10:26
# @Author  : martin.peng
# @Site    : 
# @File    : base_request.py

import re

import requests

from Config.global_dict import get_api_server_config, set_value

restFulReplaceKeyDict = {'{apiKey}': 'api_key', '{secret}': 'secret'}


class RestFulReplace:
    @classmethod
    def url_replace(cls, params: str):
        for key, value in restFulReplaceKeyDict.items():
            if params.find(key) >= 0:
                api_server_config = get_api_server_config()
                # params = re.match(r'\{.*?\}', params)
                params = re.sub(r'\{.*?\}', getattr(api_server_config, value), params)
        return params


class BaseRequest:
    path: str
    method: str
    content_type: str
    params: dict
    body: any
    host: str
    response: str
    response_code: int
    need_response: bool
    headers: dict

    def __init__(self, title, path, method, params: dict, body: any, host, headers: dict, need_response):
        self.path = RestFulReplace.url_replace(path)
        self.method = method
        self.params = params
        self.host = host
        self.need_response = need_response
        self.headers = headers
        self.body = body
        self.title = title
        if params is not None:
            for key, value in params.items():
                _value = value
                if type(_value) == dict:
                    for __key in _value.keys():
                        _value = '{' + __key + '}'
                params[key] = RestFulReplace.url_replace(_value)

    def execute_request(self):
        response = requests.request(method=self.method
                                    , url=self.host + self.path
                                    , params=self.params
                                    , headers=self.headers
                                    , data=self.body)
        assert response.status_code == 200
        if self.need_response:
            set_value(self.title, response.text)
