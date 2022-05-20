#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 11:27
# @Author  : martin.peng
# @Site    : 
# @File    : get_auth_id_script.py
from requests.models import Response


def post_script(response: Response):
    assert response.status_code == 404
    response_json = response.json()[0]
    assert response_json.get('httpCode') == 404
    assert response_json.get('error') == 'Path not found: /wps/rest/cart/v1/admin/getAuthId//'
