# -*- coding: utf-8 -*-

from app.app import db


class JobImportance(db.Model):
    __tablename__ = 'jobs_importance'

    quarter_id = db.Column(db.SmallInteger, db.ForeignKey('quarters.quarter_id'), primary_key=True)
    geography_id = db.Column(db.SmallInteger, db.ForeignKey('geographies.geography_id'), primary_key=True)
    job_uuid = db.Column(db.String, primary_key=True)
    importance = db.Column(db.Float)

    def __repr__(self):
        return '<JobImportance {}/{}/{}>'.format(
            self.geography_id, self.quarter_id, self.job_uuid
        )
