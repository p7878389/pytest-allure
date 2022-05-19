#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 10:26
# @Author  : martin.peng
# @Site    : 
# @File    : base_request.py
import json
import re

from Config.global_dict import get_value, get_replace_dict_all


class RestFulReplace:
    @classmethod
    def params_replace(cls, params: str):
        for key, value in get_replace_dict_all().items():
            if params.find(key) >= 0:
                if value is None or value == '':
                    value = key[1, len(key) - 1]
                params = re.sub(r'' + key, get_value(value), params)
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
    headers: {}

    # origin_headers: dict

    def __init__(self, title, path, method, params: dict, body: any, host, headers: {}):
        self.path = RestFulReplace.params_replace(path)
        self.method = method
        self.params = params
        self.host = host
        self.headers = headers
        self.body = body
        self.title = title
        self.parse_body_content()
        if params is not None:
            params_json = json.dumps(params)
            params_json = RestFulReplace.params_replace(params_json)
            params = json.loads(params_json)
            self.params = params
        if headers is not None:
            headers_json = json.dumps(headers)
            headers_json = RestFulReplace.params_replace(headers_json)
            headers = json.loads(headers_json)
            self.headers = headers

    def parse_body_content(self):
        if self.body is None or self.body == '':
            return
        content_type = self.headers.get('Content-Type')
        if content_type is None or content_type == '':
            return
        content_type = content_type.lower()
        if content_type == 'application/json':
            json_body = json.dumps(self.body)
            self.body = RestFulReplace.params_replace(json_body)
