#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/17 11:39
# @Author  : martin.peng
# @Site    : 
# @File    : api.py
import json
from urllib import parse


class ApiServerConfig:

    def __init__(self, d):
        self.host = str
        self.api_Key = str
        self.secret = str
        self.__dict__ = d
        if self.__dict__.get('secret'):
            self.encodeSecret = parse.quote(self.__dict__.get('secret'))


class FileDataConfig:

    def __init__(self, d):
        self.case_file_path = None
        self.report_data_file_path = None
        self.report_generate_file_data = None
        self.report_zip_file_path = None
        self.__dict__ = d


class LoggingConfig:

    def __init__(self, d):
        self.log_file_path = str
        self.log_file_name = ''
        self.log_level = 0
        self.log_format = ''
        self.__dict__ = d


class ApiCase:
    def __init__(self, d):
        self.title = str
        self.host = str
        self.path = str
        self.params = {}
        self.headers = {}
        self.method = str
        self.body = ''
        self.feature = any
        self.story = any
        self.description = any
        self.need_response = False
        self.skip = False
        self.response_script = str
        self.__dict__ = d

    def __str__(self) -> str:
        return json.dumps(self.__dict__)
