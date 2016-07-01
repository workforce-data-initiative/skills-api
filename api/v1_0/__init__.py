# -*- coding: utf-8 -*-

"""
api.v1_0
~~~~~~~~
"""

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_v1_0', __name__)
api = Api(api_bp)

from . models.skills_master import SkillMaster
from . models.skills_related import SkillRelated
from . models.jobs_master import JobMaster
from . models.jobs_alternate_titles import JobAlternateTitle
from . models.jobs_unusual_titles import JobUnusualTitle
from . models.jobs_skills import JobSkill

from . endpoints import *

# endpoints go here
api.add_resource(JobTitleNormalizeEndpoint, '/2')
api.add_resource(JobTitleFromONetCodeEndpoint, '/3')
api.add_resource(SkillNameAutocompleteEndpoint, '/4')
api.add_resource(NormalizeSkillNameEndpoint, '/5')
api.add_resource(NormalizedSkillUUIDFromONetCodeEndpoint, '/6')
api.add_resource(AssociatedSkillsForJobEndpoint, '/7')
api.add_resource(AssociatedJobsForJobEndpoint, '/8')
api.add_resource(AssociatedSkillForSkillEndpoint, '/9')
api.add_resource(SkillNameAndFrequencyEndpoint, '/10')
api.add_resource(JobNameFromUUIDEndpoint, '/11')
api.add_resource(AllJobsEndpoint, '/jobs')
api.add_resource(AllSkillsEndpoint, '/skills')
api.add_resource(JobTitleAutocompleteEndpoint, '/jobs/autocomplete')