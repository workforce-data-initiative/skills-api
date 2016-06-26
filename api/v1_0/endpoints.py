# -*- coding: utf-8 -*-

"""
api.v1_0.endpoints
~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request
from flask_restful import Resource

class TestEndPoint(Resource):
    def get(self):
        return 'wii would like to play'
