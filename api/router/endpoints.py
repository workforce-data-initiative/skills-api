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
        return route_api('jobtitleautocompleteendpoint')

class SkillNameAutocompleteEndpoint(Resource):
    def get(self):
        return route_api('skillnameautocompleteendpoint')

class JobTitleNormalizeEndpoint(Resource):
    def get(self):
        return route_api('jobtitlenormalizeendpoint')

class JobTitleFromONetCodeEndpoint(Resource):
    def get(self, id=None):
        return route_api('jobtitlefromonetcodeendpoint', id=id)

class NormalizeSkillNameEndpoint(Resource):
    def get(self):
        return route_api('normalizeskillnameendpoint')

class NormalizedSkillUUIDFromONetCodeEndpoint(Resource):
    def get(self):
        pass

class AssociatedSkillsForJobEndpoint(Resource):
    def get(self, id):
        return route_api('associatedskillsforjobendpoint', id=id)
        
class AssociatedJobsForSkillEndpoint(Resource):
    def get(self, id):
        return route_api('associatedjobsforskillendpoint', id=id)

class AssociatedJobsForJobEndpoint(Resource):
    def get(self):
        pass

class AssociatedSkillForSkillEndpoint(Resource):
    def get(self):
        pass

class SkillNameAndFrequencyEndpoint(Resource):
    def get(self, id=None):
        return route_api('skillnameandfrequencyendpoint', id=id)