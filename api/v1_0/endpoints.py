# -*- coding: utf-8 -*-

"""
api.v1_0.endpoints
~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request
from flask_restful import Resource

class JobTitleAutocompleteEndpoint(Resource):
    def get(self):
        return "endpoint 1"

class JobTitleNormalizeEndpoint(Resource):
    def get(self):
        return "endpoint 2"

class JobTitleFromONetCodeEndpoint(Resource):
    def get(self):
        return "endpoint 3"

class SkillNameAutocompleteEndpoint(Resource):
    def get(self):
        return "endpoint 4"

class NormalizeSkillNameEndpoint(Resource):
    def get(self):
        return "endpoint 5"

class NormalizedSkillUUIDFromONetCodeEndpoint(Resource):
    def get(self):
        return "endpoint 6"

class AssociatedSkillsForJobEndpoint(Resource):
    def get(self):
        return "endpoint 7"

class AssociatedJobsForJobEndpoint(Resource):
    def get(self):
        return "endpoint 8"

class AssociatedSkillForSkillEndpoint(Resource):
    def get(self):
        return "endpoint 9"

class SkillNameAndFrequencyEndpoint(Resource):
    def get(self):
        return "endpoint 10"

class JobNameFromUUIDEndpoint(Resource):
    def get(self):
        return "endpoint 11"

class AllJobsEndpoint(Resource):
    def get(self):
        return "endpoint 12"

class AllSkillsEndpoint(Resource):
    def get(self):
        return "endpoint 13"

class TestEndPoint(Resource):
    def get(self):
        return 'wii would like to play'
