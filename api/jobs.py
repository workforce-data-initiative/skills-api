# -*- coding: utf-8 -*-

"""
api.resources.jobs
~~~~~~~~~~~~~~~~~~
Definitions of all methods associated with jobs endpoints.
"""

from flask import abort
from flask_restful import Resource
from app.app import db
from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills

import json

class Job(Resource):
    def get(self, id):
        output = {}
        result = SkillsMaster.query.filter_by(skill_uuid = id).first()
        if result:
            output['skill_name'] = result.skill_name
            output['count'] = result.count
            return output
        else:
            abort(404)
