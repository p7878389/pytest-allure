#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 15:21
# @Author  : martin.peng
# @Site    : 
# @File    : prepare_payments_script.py

import json

from BaseRequest.base_request import RestFulReplace
from Config.global_dict import get_value
from Model.api import ApiCase


def pre_script_prepare_payments(api_case: ApiCase):
    prepare_transaction_json = json.loads(get_value('prepare_transaction'))
    _payments = api_case.body['payments']
    _payments = RestFulReplace.params_replace(json.dumps(_payments))
    _payments = json.loads(_payments)
    prepare_transaction_json['payments'] = _payments
    api_case.body = prepare_transaction_json
