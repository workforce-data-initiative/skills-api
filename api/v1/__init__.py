# -*- coding: utf-8 -*-

"""API Version 1

This package contains all the endpoints and data models for the version 1 API.

"""

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)

from . models.skills_master import SkillMaster
from . models.skills_related import SkillRelated
from . models.jobs_master import JobMaster
from . models.jobs_alternate_titles import JobAlternateTitle
from . models.jobs_unusual_titles import JobUnusualTitle
from . models.jobs_skills import JobSkill
from . models.skills_importance import SkillImportance

from . endpoints import *

# ------------------------------------------------------------------------
# API Version 1 Endpoints 
# ------------------------------------------------------------------------
api.add_resource(AllJobsEndpoint, '/jobs')
api.add_resource(AllSkillsEndpoint, '/skills')
api.add_resource(JobTitleAutocompleteEndpoint, '/jobs/autocomplete')
api.add_resource(SkillNameAutocompleteEndpoint, '/skills/autocomplete')
api.add_resource(JobTitleNormalizeEndpoint, '/jobs/normalize')
api.add_resource(AllUnusualJobsEndpoint, '/jobs/unusual_titles')
api.add_resource(NormalizeSkillNameEndpoint, '/skills/normalize')
api.add_resource(JobTitleFromONetCodeEndpoint, '/jobs/<string:id>')
api.add_resource(SkillNameAndFrequencyEndpoint, '/skills/<string:id>')
api.add_resource(AssociatedSkillsForJobEndpoint, '/jobs/<string:id>/related_skills')
api.add_resource(AssociatedJobsForSkillEndpoint, '/skills/<string:id>/related_jobs')
api.add_resource(AssociatedJobsForJobEndpoint, '/jobs/<string:id>/related_jobs')
api.add_resource(AssociatedSkillForSkillEndpoint, '/skills/<string:id>/related_skills')
