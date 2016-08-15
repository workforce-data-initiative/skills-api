# -*- coding: utf-8 -*-

"""API Router Package.

The router package provides a simple façade for handing versions of the API.
When a version is not specified via the endpoint (e.g. /v1/foo/bar) the router
is responsible for determining what version of the API should be used.   

"""

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_router', __name__)
api = Api(api_bp)

from . endpoints import *

# ------------------------------------------------------------------------
# API Version 1 Endpoints 
# ------------------------------------------------------------------------
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