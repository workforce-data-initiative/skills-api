# -*- coding: utf-8 -*-

"""
api.v1_0
~~~~~~~~
"""

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_router', __name__)
api = Api(api_bp)

from . endpoints import *

# endpoints go here
api.add_resource(AllJobsEndpoint, '/jobs')
api.add_resource(AllSkillsEndpoint, '/skills')
api.add_resource(JobTitleAutocompleteEndpoint, '/jobs/autocomplete')
api.add_resource(SkillNameAutocompleteEndpoint, '/skills/autocomplete')
api.add_resource(JobTitleNormalizeEndpoint, '/jobs/normalize')
api.add_resource(NormalizeSkillNameEndpoint, '/skills/normalize')
api.add_resource(JobTitleFromONetCodeEndpoint, '/jobs/<string:id>')
api.add_resource(SkillNameAndFrequencyEndpoint, '/skills/<string:id>')
api.add_resource(AssociatedSkillsForJobEndpoint, '/jobs/<string:id>/related_skills')
api.add_resource(AssociatedJobsForSkillEndpoint, '/skills/<string:id>/related_jobs')
api.add_resource(AssociatedJobsForJobEndpoint, '/jobs/<string:id>/related_jobs')
api.add_resource(AssociatedSkillForSkillEndpoint, '/skills/<string:id>/related_skills')