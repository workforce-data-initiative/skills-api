# -*- coding: utf-8 -*-

"""
common.utils
~~~~~~~~~~~~

"""
import re
import json
import functools
from flask import request, make_response, redirect, url_for
from collections import OrderedDict

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

def create_response(data, status, custom_headers=None):
    response = make_response(json.dumps(data), status)
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Origin'] = "*"

    if custom_headers is not None:
        for custom_header in custom_headers:
            header = custom_header.strip().split('=')
            response.headers[header[0]] = header[1]

    return response

def create_error(data, status):
    response_obj = {}
    response_obj['error'] = OrderedDict()
    response_obj['error']['code'] = status
    response_obj['error']['message'] = data
    response = make_response(json.dumps(response_obj), status)
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Origin'] = "*"

    return response

def route_api(endpoint_class, id=None):
    api_version = get_api_version_custom()
    if api_version is not None:
        endpoint = 'api_v' + normalize_version_number(api_version) + '.' + endpoint_class
        return redirect(url_for(endpoint, id=id, **request.args))
    else:
        api_version = get_api_version_accept()
        if api_version is not None:
            endpoint = 'api_v' + normalize_version_number(parse_version_number(api_version)) + '.' + endpoint_class
            return redirect(url_for(endpoint, id=id, **request.args))
        else:
            return create_error('A version header is missing from the request', 400)
