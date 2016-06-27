# -*- coding: utf-8 -*-

"""
api.v1_0
~~~~~~~~
"""

from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api_v1_1', __name__)
api = Api(api_bp)

from .. v1_0.models.skills_master import SkillMaster
from .. v1_0.models.skills_related import SkillRelated
from .. v1_0.models.jobs_master import JobMaster
from .. v1_0.models.jobs_alternate_titles import JobAlternateTitle

from . endpoints import TestEndPoint

# endpoints go here
api.add_resource(TestEndPoint, '/foo')

