#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 15:21
# @Author  : martin.peng
# @Site    : 
# @File    : prepare_transaction_script.py
import json

from requests.models import Response

from Config.global_dict import set_value, set_replace_key_dict


# def pre_script_prepare_transaction(api_case: ApiCase):
#     api_case[headers]


def post_script_prepare_transaction(response: Response):
    assert response.status_code == 200
    set_value('prepare_transaction', json.dumps(response.json()))
    set_replace_key_dict('"{prepare_transaction}"', 'prepare_transaction')
