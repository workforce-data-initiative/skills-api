# -*- coding: utf-8 -*-

from app.app import db


class Geography(db.Model):
    __tablename__ = 'geographies'

    geography_id = db.Column(db.SmallInteger, primary_key=True)
    geography_type = db.Column(db.String, nullable=False)
    geography_name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<geography {}/{}>'.format(
            self.geography_type, self.geography_name
        )
