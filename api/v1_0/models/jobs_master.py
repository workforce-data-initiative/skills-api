# -*- coding: utf-8 -*-

"""
api.version.v1_0.models.jobs_master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from app.app import db

class JobMaster(db.Model):
    __tablename__ = 'jobs_master'

    uuid = db.Column(db.String, primary_key=True)
    onet_soc_code = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    alternate_titles = db.relationship('JobAlternateTitle', backref='job', lazy='dynamic')

    def __init__(self, uuid, onet_soc_code, title, description):
        self.uuid = uuid
        self.onet_soc_code = onet_soc_code
        self.title = title
        self.description = description

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
