
# -*- coding: utf-8 -*-

"""
db.models.related_skills
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Job_Skills database table.
"""

from app.app import db
from sqlalchemy.dialects.postgresql import JSONB


class JobSkills(db.Model):
    __tablename__ = 'job_skills'
    
    #skill_uuid = db.Column(db.Integer, primary_key=True)
    onet_soc_code = db.Column(db.String, primary_key=True)
    related_skills = db.Column(JSONB)

    def __init__(self, onet_soc_code, related_skills):
        self.onet_soc_code = onet_soc_code
        self.related_skills = related_skills

    def __repr__(self):
        return '<onet_soc_code {}>'.format(self.onet_soc_code)
