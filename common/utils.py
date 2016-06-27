# -*- coding: utf-8 -*-

"""
commun.utils
~~~~~~~~~~~~

"""
import re
from flask import request

def get_api_version_custom():
    return request.headers.get('api-version')


def get_api_version_accept():
    return request.headers.get('accept')

def parse_version_number(header):
    version_regex = '\w+/[VvNnDd]{3}\.\w+\.v([0-9\.]+)\+'
    match = re.search(version_regex, header)
    if match:
        found = match.group(1)
    else:
        found = None

    return found

def normalize_version_number(version_number):
    return version_number.replace('.', '_') 

