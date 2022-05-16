#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:40
# @Author  : martin.peng
# @Site    : 
# @File    : runner.py
import os
from os.path import dirname, abspath

from BaseRequest.base_request import RestFulReplace
from Config.global_dict import dict_init, get_file_path_config
from Config.yaml_read import load_yaml


def runner_init():
    dict_init()
    environ_name = os.environ.get("pytest-allure-environ");
    if environ_name is None or not environ_name.isspace():
        environ_name = 'test'
    project_root = dirname(dirname(abspath(__file__)))
    system_config_file_path = os.path.join(project_root, 'Config\\' + 'config-' + environ_name + '.yml')
    load_yaml(system_config_file_path)


if __name__ == '__main__':
    runner_init()
    print(get_file_path_config())
    RestFulReplace.url_replace(params="sss/{{apiKey}}")
