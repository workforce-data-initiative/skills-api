
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
    
    skill_uuid = db.Column(db.String, primary_key=True)
    related_jobs = db.Column(JSONB)

    def __init__(self, skill_uuid, related_jobs):
        self.skill_uuid = skill_uuid
        self.related_jobs = related_jobs

    def __repr__(self):
        return '<skill_uuid {}>'.format(self.onet_soc_code)
