
# -*- coding: utf-8 -*-

"""
db.models.related_skills
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Related_Skills database table.
"""

from app.app import db
from sqlalchemy.dialects.postgresql import JSONB


class RelatedSkill(db.Model):
    __tablename__ = 'related_skills'
    
    uuid = db.Column(db.String, primary_key=True)
    related_skills = db.Column(JSONB)

    def __init__(self, uuid, related_skills):
        self.uuid = uuid
        self.related_skills = related_skills

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
