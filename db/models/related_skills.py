
# -*- coding: utf-8 -*-

"""
db.models.related_skills
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Related_Skills database table.
"""

from app.app import db
from sqlalchemy.dialects.postgresql import JSONB


class RelatedSkills(db.Model):
    __tablename__ = 'related_skills'
    
    skill_uuid = db.Column(db.Integer, primary_key=True)
    related_skills = db.Column(JSONB)

    def __init__(self, skill_uuid, related_skills):
        self.skill_uuid = skill_uuid
        self.related_skills = related_skills

    def __repr__(self):
        return '<skill_uuid {}>'.format(self.skill_uuid)
