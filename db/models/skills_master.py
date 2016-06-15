
# -*- coding: utf-8 -*-

from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, String

"""
db.models.skills_master
~~~~~~~~~~~~~~~~~~~~~~~~
An ORM class representing the Skills_Master database table.
"""

class SkillsMaster(Model):
    skill_uuid = Column(Integer, primary_key=True)
    onet_element_id = Column(String)
    skill_name = Column(String)
    count = Column(Integer)
