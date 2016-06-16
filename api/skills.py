# -*- coding: utf-8 -*-

"""
api.resources.skills
~~~~~~~~~~~~~~~~~~~~
Definitions of all methods associated with skills endpoints.
"""

from flask_restful import Resource
from app.app import db
from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills

class Skill(Resource):
    def get(self):
        return 'I am pretty darn skillful'
