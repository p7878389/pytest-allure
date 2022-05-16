#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:05
# @Author  : martin.peng
# @Site    : 
# @File    : global_dict.py

_global_dict = None
api_server_config_name = "api_server_config"
file_path_config_name = "file_path_config"


def dict_init():
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    _global_dict[key] = value


def get_value(key, default_value=None):
    try:
        return _global_dict[key]
    except KeyError:
        return default_value


def set_api_server_config(value):
    set_value(api_server_config_name, value)
    # if not value is None and value is ApiServerConfig:


def get_api_server_config():
    return get_value(api_server_config_name, None)


def get_file_path_config():
    return get_value(file_path_config_name, None)


def set_file_path_config(value):
    return set_value(file_path_config_name, value)
