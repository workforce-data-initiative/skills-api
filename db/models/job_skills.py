
# -*- coding: utf-8 -*-

"""
db.models.job_skills
~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Job_Skills database table.
"""

from app.app import db
from sqlalchemy.dialects.postgresql import JSONB


class JobSkill(db.Model):
    __tablename__ = 'job_skills'
    
    uuid = db.Column(db.String, primary_key=True)
    related_jobs = db.Column(JSONB)

    def __init__(self, uuid, related_jobs):
        self.uuid = uuid
        self.related_jobs = related_jobs

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
