# -*- coding: utf-8 -*-

"""
api.skills
~~~~~~~~~~
Definitions of all methods associated with skills endpoints.
"""

from flask import abort
from flask_restful import Resource
from app.app import db
from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills

class Skill(Resource):
    def get(self, id):
        output = {}
        result = SkillsMaster.query.filter_by(skill_uuid = id).first()
        if result:
            output['skill_name'] = result.skill_name
            output['count'] = result.count
            return output
        else:
            abort(404)
