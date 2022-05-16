#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 9:31
# @Author  : martin.peng
# @Site    : 
# @File    : yaml_read.py
import string
from urllib import parse

import yaml

from Config.global_dict import set_value, set_api_server_config, set_file_path_config


def load_yaml(file_path: string):
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
    content = yaml.load(file_content, Loader=yaml.FullLoader)
    yaml_dict = {}
    yaml_dict.update(content)
    set_api_server_config(ApiServerConfig(yaml_dict['api-server']))
    set_file_path_config(FileDataConfig(yaml_dict['file_path']))
    set_value(file_path, yaml_dict)


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
        self.log_file_path = None
        self.__dict__ = d
