# -*- coding: utf-8 -*-

"""Jobs Skills ORM"""

from app.app import db

class JobSkill(db.Model):
    __tablename__ = 'jobs_skills'
    
    job_uuid = db.Column(db.String, db.ForeignKey('jobs_master.uuid'), primary_key=True)
    skill_uuid = db.Column(db.String, db.ForeignKey('skills_master.uuid'), primary_key=True)
    
    def __init__(self, job_uuid, skill_uuid):
        self.job_uuid = job_uuid
        self.skill_uuid = skill_uuid

    def __repr__(self):
        return '<uuid {}>'.format(self.job_uuid)
