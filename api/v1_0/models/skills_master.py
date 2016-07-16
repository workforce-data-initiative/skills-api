# -*- coding: utf-8 -*-

"""
api.version.v1_0.models.skill_master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from app.app import db

class SkillMaster(db.Model):
    __tablename__ = 'skills_master'

    uuid = db.Column(db.String, primary_key=True)
    onet_soc_code = db.Column(db.String)
    onet_element_id = db.Column(db.String)
    onet_ksa = db.Column(db.String)
    description = db.Column(db.String)
    nlp_a = db.Column(db.String)

    def __init__(self, uuid, onet_soc_code, onet_element_id, onet_ksa, description, nlp_a):
        self.uuid = uuid
        self.onet_soc_code = onet_soc_code
        self.onet_element_id = onet_element_id
        self.onet_ksa = onet_ksa
        self.description = description
        self.nlp_a = nlp_a

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
