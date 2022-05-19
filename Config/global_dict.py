#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/16 15:05
# @Author  : martin.peng
# @Site    : 
# @File    : global_dict.py
from Model.api import ApiServerConfig, LoggingConfig

_global_dict = {}
api_server_config_name = "api_server_config"
file_path_config_name = "file_path_config"
logging_config_name = "logging_config"
rest_ful_replace_key_dict = {'{apiKey}': 'api_key', '{secret}': 'secret', '{token}': 'token'}


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


def set_api_server_config(value: ApiServerConfig):
    set_value(api_server_config_name, value)
    set_value('api_key', value.api_key)
    set_value('secret', value.secret)


def get_api_server_config():
    return get_value(api_server_config_name, None)


def get_file_path_config():
    return get_value(file_path_config_name, None)


def set_file_path_config(value):
    return set_value(file_path_config_name, value)


def get_logging_config() -> LoggingConfig:
    return get_value(logging_config_name, None)


def set_logging_config(value: LoggingConfig):
    return set_value(logging_config_name, value)
