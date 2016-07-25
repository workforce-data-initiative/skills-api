# -*- coding: utf-8 -*-

"""
api.version.v1_0.models.skill_related
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from app.app import db
from sqlalchemy.dialects.postgresql import JSONB

class SkillRelated(db.Model):
    __tablename__ = 'skills_related'

    uuid = db.Column(db.String, primary_key=True)
    related_skills = db.Column(JSONB)

    def __init__(self, uuid, related_skills):
        self.uuid = uuid
        self.related_skills = related_skills     

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
