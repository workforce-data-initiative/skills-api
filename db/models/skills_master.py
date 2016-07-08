# -*- coding: utf-8 -*-

"""
db.models.skills_master
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Skills_Master database table.
"""

from app.app import db

class SkillMaster(db.Model):
    __tablename__ = 'skills_master'
    
    uuid = db.Column(db.String, primary_key=True)
    onet_soc_code = db.Column(db.String)
    onet_element_id = db.Column(db.String)
    skill_name = db.Column(db.String)
    count = db.Column(db.Integer)

    def __init__(self, uuid, onet_soc_code, onet_element_id, skill_name, count):
        self.uuid = uuid
        self.onet_soc_code = onet_soc_code
        self.onet_element_id = onet_element_id
        self.skill_name = skill_name
        self.count = count

    def __repr__(self):
        return '<uuid {}>'.format(self.uuid)
