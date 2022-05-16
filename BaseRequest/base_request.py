#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 10:26
# @Author  : martin.peng
# @Site    : 
# @File    : base_request.py

import re

import requests

from Config.global_dict import get_api_server_config

restFulReplaceKeyDict = {'{{apiKey}}': 'api_key'}


class RestFulReplace:
    @classmethod
    def url_replace(cls, params: str):
        for key, value in restFulReplaceKeyDict.items():
            if params.index(key) >= 0:
                api_server_config = get_api_server_config()
                params = re.sub(r'\{{.*?\}}', getattr(api_server_config, value), params)
                print(params)
        return params


class BaseRequest(RestFulReplace):
    path: str
    method: str
    content_type: str
    params: dict
    body: object
    host: str
    response: str
    response_code: int
    need_response: bool

    def __init__(self, path, method, content_type, params, host, need_response):
        self.path = path
        self.method = method
        self.content_type = content_type
        self.params = params
        self.host = host
        self.need_response = need_response

    def base_request(self, _headers: dict):
        _headers['content_type'] = self.content_type
        return requests.request(method=self.method
                                , url=self.host + self.path
                                , params=self.params
                                , headers=_headers
                                , data=self.body)
