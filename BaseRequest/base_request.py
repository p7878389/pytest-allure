#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 10:26
# @Author  : martin.peng
# @Site    : 
# @File    : base_request.py
import json
import re

from Config.global_dict import get_value, rest_ful_replace_key_dict


class RestFulReplace:
    @classmethod
    def url_replace(cls, params: str):
        for key, value in rest_ful_replace_key_dict.items():
            if params.find(key) >= 0:
                if value is None or value == '':
                    value = key[1, len(key) - 1]
                params = re.sub(r'\{.*?\}', get_value(value), params)
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
        self.path = RestFulReplace.url_replace(path)
        self.method = method
        self.params = params
        self.host = host
        self.headers = headers
        self.body = body
        self.title = title
        self.parse_body_content()
        if params is not None:
            for key, value in params.items():
                _value = value
                if type(_value) == dict:
                    for __key in _value.keys():
                        _value = '{' + __key + '}'
                params[key] = RestFulReplace.url_replace(_value)
        if headers is not None:
            for key, value in headers.items():
                _value = value
                if type(_value) == dict:
                    for __key in _value.keys():
                        _value = '{' + __key + '}'
                headers[key] = RestFulReplace.url_replace(_value)

    def parse_body_content(self):
        if self.body is None or self.body == '':
            return
        content_type = self.headers.get('Content-Type')
        if content_type is None or content_type == '':
            return
        content_type = content_type.lower()
        if content_type == 'application/json':
            json_body = json.dumps(self.body)
            self.body = RestFulReplace.url_replace(json_body)
