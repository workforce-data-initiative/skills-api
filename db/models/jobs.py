# -*- coding: utf-8 -*-

"""
db.models.jobs
~~~~~~~~~~~~~~
An ORM class representing the Jobs database table.
"""

from app.app import db

class Job(db.Model):
    __tablename__ = 'jobs'
    
    uuid = db.Column(db.String, primary_key=True)
    onet_soc_code = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    alternate_titles = db.relationship('AlternateJobTitle', backref='job', lazy='dynamic')
    
    def __init__(self, job_uuid, onet_soc_code, title, description):
        self.job_uuid = job_uuid
        self.onet_soc_code = onet_soc_code
        self.title = title
        self.description = description
        
    def __repr__(self):
        return '<uuid {}>'.format(self.job_uuid)

class AlternateJobTitle(db.Model):
    __tablename__ = 'alternate_job_titles'
    
    uuid = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    job_uuid = db.Column(db.String, db.ForeignKey('jobs.uuid'))
    
    def __init__(self, uuid, title, job_uuid):
        self.uuid = uuid
        self.title = title
        self.job_uuid = job_uuid
        
    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
