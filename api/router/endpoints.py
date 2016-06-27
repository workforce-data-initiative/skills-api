# -*- coding: utf-8 -*-

"""
api.router.endpoints
~~~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request, redirect, url_for
from flask_restful import Resource
from common.utils import *


class JobTitleAutocompleteEndpoint(Resource):
    def get(self):
        pass

class JobTitleNormalizeEndpoint(Resource):
    def get(self):
        pass

class JobTitleFromONetCodeEndpoint(Resource):
    def get(self):
        pass

class SkillNameAutocompleteEndpoint(Resource):
    def get(self):
        pass

class NormalizeSkillNameEndpoint(Resource):
    def get(self):
        pass

class NormalizedSkillUUIDFromONetCodeEndpoint(Resource):
    def get(self):
        pass

class AssociatedSkillsForJobEndpoint(Resource):
    def get(self):
        pass

class AssociatedJobsForJobEndpoint(Resource):
    def get(self):
        pass

class AssociatedSkillForSkillEndpoint(Resource):
    def get(self):
        pass

class SkillNameAndFrequencyEndpoint(Resource):
    def get(self):
        pass

class JobNameFromUUIDEndpoint(Resource):
    def get(self):
        pass

class AllJobsEndpoint(Resource):
    def get(self):
        pass

class AllSkillsEndpoint(Resource):
    def get(self):
        pass

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
