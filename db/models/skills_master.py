# -*- coding: utf-8 -*-

"""
db.models.skills_master
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Skills_Master database table.
"""

from app.app import db

class SkillsMaster(db.Model):
    __tablename__ = 'skills_master'
    
    skill_uuid = db.Column(db.Integer, primary_key=True)
    onet_element_id = db.Column(db.String)
    skill_name = db.Column(db.String)
    count = db.Column(db.Integer)
