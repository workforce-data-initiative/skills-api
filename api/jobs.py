# -*- coding: utf-8 -*-

"""
api.jobs
~~~~~~~~~
Definitions of all methods associated with jobs endpoints.
"""

from flask import abort
from flask_restful import Resource
from app.app import db
#from db.models.skills_master import SkillsMaster
#from db.models.related_skills import RelatedSkills
from db.models.job_skills import JobSkills

class JobSkill(Resource):
    def get(self, id):
        output = {}
        result = JobSkills.query.filter_by(onet_soc_code = id).first()
        if result:
            return result.related_skills
        else:
            abort(404)
