# -*- coding: utf-8 -*-

from app.app import db


class Quarter(db.Model):
    __tablename__ = 'quarters'

    quarter_id = db.Column(db.SmallInteger, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Quarter {}/{}>'.format(
            self.year, self.quarter
        )
