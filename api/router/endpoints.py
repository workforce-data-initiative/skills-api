# -*- coding: utf-8 -*-

"""
api.router.endpoints
~~~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request, redirect, url_for
from flask_restful import Resource
from common.utils import *

class AllJobsEndpoint(Resource):
    def get(self):
        return route_api('alljobsendpoint')

class AllSkillsEndpoint(Resource):
    def get(self):
        return route_api('allskillsendpoint')

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