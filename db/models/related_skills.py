
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
