# -*- coding: utf-8 -*-

"""
api.version.v1_0.models.jobs_alternate_titles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from app.app import db

class JobAlternateTitle(db.Model):
    __tablename__ = 'jobs_alternate_titles'

    uuid = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    job_uuid = db.Column(db.String, db.ForeignKey('jobs_master.uuid'))
            
    def __init__(self, uuid, title, job_uuid):
        self.uuid = uuid
        self.title = title
        self.job_uuid = job_uuid

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
