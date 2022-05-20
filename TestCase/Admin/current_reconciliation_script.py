#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 9:22
# @Author  : martin.peng
# @Site    : 
# @File    : current_reconciliation_script.py
from requests.models import Response


def current_reconciliation_post_script(response: Response):
    assert response.status_code == 403
    response_json = response.json()[0]
    assert response_json.get('httpCode') == 403
    assert response_json.get('error') == "Client '1' not found or you don't have permission for them."
