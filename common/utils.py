# -*- coding: utf-8 -*-

"""General Purpose Utilites"""

import re
import json
import functools
from flask import request, make_response, redirect, url_for
from collections import OrderedDict

def get_api_version_custom():
    """Retrieve custom version header from HTTP request.

    Returns:
        Content of the api-version custom header.

    """
    return request.headers.get('api-version')


def get_api_version_accept():
    """Retrieve accept header from HTTP request.
    
    Returns:
        Content of the accept header.
    """
    return request.headers.get('accept')

def parse_version_number(header):
    """Parses the version number from an accept header
    Args:
        header (str): Header content to parse for version number.

    Returns:
        Version number.
    
    """
    version_regex = '\w+/[VvNnDd]{3}\.\w+\.v([0-9\.]+)\+'
    match = re.search(version_regex, header)
    if match:
        found = match.group(1)
    else:
        found = None

    return found

def normalize_version_number(version_number):
    """Clean up the version number extracted from the header
    Args:
        version_number (str): Version number to normalize.

    Returns:
        The normalized version number.

    """
    return version_number.replace('.', '_') 

def create_response(data, status, custom_headers=None):
    """Create a custom JSON response.
    Args:
        data (dict): Data to place in to the custom response body.
        status (str): HTTP status code to return with the response.
        custom_headers (list): Any optional custom headers to return with the response.

    Returns:
        Custom JSON response.

    """
    response = make_response(json.dumps(data), status)
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token"
    response.headers['Access-Control-Allow-Methods'] = "*"
    response.headers['Access-Control-Allow-Origin'] = "*"

    if custom_headers is not None:
        for custom_header in custom_headers:
            header = custom_header.strip().split('=')
            response.headers[header[0].strip()] = header[1].strip()

    return response

def create_error(data, status, custom_headers=None):
    """Create a custom JSON error response.
    Args:
        data (dict): Data to place in the custom response body.
        status (str): HTTP status code to return with the response.

    Returns:
        Custom JSON error response.

    """
    response_obj = {}
    response_obj['error'] = OrderedDict()
    response_obj['error']['code'] = status
    response_obj['error']['message'] = data

    return create_response(response_obj, status, custom_headers)

def route_api(endpoint_class, id=None):
    """Routes an API call based on its endpoint class and version.
    
    Args:
        endpoint_class (str): Name of endpoint class to route the API to.
        id (str): An optional ID parameter to pass to the appropriate endpoint.

    Returns:
        A redirect to the appropriate API endpoint based on its version number. 

    """
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
