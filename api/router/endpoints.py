# -*- coding: utf-8 -*-

"""
api.router.endpoints
~~~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request, redirect, url_for
from flask_restful import Resource
from common.utils import get_api_version_custom

class TestEndPoint(Resource):
    def get(self):
        api_version = get_api_version_custom()
        if api_version is not None:
            api_version = api_version.replace('.', '_')
            endpoint = 'api_v' + api_version + '.testendpoint'
            return redirect(url_for(endpoint))
