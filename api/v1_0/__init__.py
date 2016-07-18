# -*- coding: utf-8 -*-

"""
api.v1_0
~~~~~~~~
"""

from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger

API_DESCRIPTION = "a complete and standard data store for canonical and emerging " + \
                    "skills, knowledge, abilities, tools, technolgies, and how " + \
                    "they relate to jobs."

api_bp = Blueprint('api_v1_0', __name__)
api = swagger.docs(Api(api_bp), apiVersion='1.0', swaggerVersion='2.0', description=API_DESCRIPTION)

from . models.skills_master import SkillMaster
from . models.skills_related import SkillRelated
from . models.jobs_master import JobMaster
from . models.jobs_alternate_titles import JobAlternateTitle
from . models.jobs_unusual_titles import JobUnusualTitle
from . models.jobs_skills import JobSkill

from . endpoints import *

# endpoints go here
api.add_resource(AllJobsEndpoint, '/jobs', endpoint='jobs_ep')
api.add_resource(AllSkillsEndpoint, '/skills', endpoint='skills_ep')
api.add_resource(JobTitleAutocompleteEndpoint, '/jobs/autocomplete', endpoint='jobs_autocomplete_ep')
api.add_resource(SkillNameAutocompleteEndpoint, '/skills/autocomplete', endpoint='skills_autocomplete_ep')
api.add_resource(JobTitleNormalizeEndpoint, '/jobs/normalize', endpoint='jobs_normalize_ep')
api.add_resource(AllUnusualJobsEndpoint, '/jobs/unusual_titles', endpoint='jobs_unusual_titles_ep')
api.add_resource(NormalizeSkillNameEndpoint, '/skills/normalize', endpoint='skills_normalize_ep')
api.add_resource(JobTitleFromONetCodeEndpoint, '/jobs/<string:id>', endpoint='job_ep')
api.add_resource(SkillNameAndFrequencyEndpoint, '/skills/<string:id>', endpoint='skill_ep')
api.add_resource(AssociatedSkillsForJobEndpoint, '/jobs/<string:id>/related_skills', endpoint='job_skill_ep')
api.add_resource(AssociatedJobsForSkillEndpoint, '/skills/<string:id>/related_jobs', endpoint='skill_job_ep')
api.add_resource(AssociatedJobsForJobEndpoint, '/jobs/<string:id>/related_jobs', endpoint='job_job_ep')
api.add_resource(AssociatedSkillForSkillEndpoint, '/skills/<string:id>/related_skills', endpoint='skill_skill_ep')
