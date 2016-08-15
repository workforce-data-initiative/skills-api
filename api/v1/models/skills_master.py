# -*- coding: utf-8 -*-

"""Skills Master ORM"""

from app.app import db

class SkillMaster(db.Model):
    __tablename__ = 'skills_master'

    uuid = db.Column(db.String, primary_key=True)
    skill_name = db.Column(db.String)
    onet_element_id = db.Column(db.String)
    description = db.Column(db.String)
    nlp_a = db.Column(db.String)

    def __init__(self, uuid, skill_name, onet_element_id, description, nlp_a):
        self.uuid = uuid
        self.skill_name = skill_name
        self.onet_element_id = onet_element_id
        self.description = description
        self.nlp_a = nlp_a

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
