# -*- coding: utf-8 -*-

from app.app import db


class GeoTitleCount(db.Model):
    __tablename__ = 'geo_title_counts'

    quarter_id = db.Column(db.SmallInteger, db.ForeignKey('quarters.quarter_id'), primary_key=True)
    geography_id = db.Column(db.SmallInteger, db.ForeignKey('geographies.geography_id'), primary_key=True)
    job_uuid = db.Column(db.String, primary_key=True)
    job_title = db.Column(db.String)
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<GeoTitleCount {}/{}/{}: {}>'.format(
            self.geography_id, self.quarter_id, self.job_uuid, self.count
        )
