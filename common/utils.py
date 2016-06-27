# -*- coding: utf-8 -*-

"""
commun.utils
~~~~~~~~~~~~

"""

from flask import request

def get_api_version_custom():
    return request.headers.get('api-version')


def get_api_version_accept():
    pass
