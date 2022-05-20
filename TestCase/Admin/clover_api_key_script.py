#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 13:47
# @Author  : martin.peng
# @Site    : 
# @File    : clover_api_key_script.py

from requests.models import Response


def post_script(response: Response):
    assert response.status_code == 200
    assert response.text.find('No Clover ApiKey configured for Client with UUID') >= 0
