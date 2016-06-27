# -*- coding: utf-8 -*-

"""
api.router.endpoints
~~~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request, redirect, url_for
from flask_restful import Resource
from common.utils import *

class TestEndPoint(Resource):
    def get(self):
        api_version = get_api_version_custom()
        if api_version is not None:
            endpoint = 'api_v' + normalize_version_number(api_version) + \
                    '.testendpoint'
            return redirect(url_for(endpoint))
        else:
            api_version = get_api_version_accept()
            if api_version is not None:
                endpoint = 'api_v' + normalize_version_number(parse_version_number(api_version)) + '.testendpoint'
                return redirect(url_for(endpoint))
