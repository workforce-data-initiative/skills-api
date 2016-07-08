# -*- coding: utf-8 -*-

"""
api.resources.jobs
~~~~~~~~~~~~~~~~~~
Definitions of all methods associated with jobs endpoints.
"""

from flask_restful import Resource

class Job(Resource):
    def get(self):
        return 'I am just a job. A simple little job.'