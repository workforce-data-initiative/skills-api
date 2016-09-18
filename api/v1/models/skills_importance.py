# -*- coding: utf-8 -*-

"""Skills Importance ORM"""

from app.app import db

class SkillImportance(db.Model):
	__tablename__ = 'skills_importance'

	job_uuid = db.Column(db.String, db.ForeignKey('jobs_master.uuid'), primary_key=True)
	skill_uuid = db.Column(db.String, db.ForeignKey('skills_master.uuid'), primary_key=True)
	level = db.Column(db.Float)
	importance = db.Column(db.Float)


	def __init__(self, job_uuid, skill_uuid, level, importance):
		self.job_uuid = job_uuid
		self.skill_uuid = skill_uuid
		self.level = level
		self.importance = importance

	def __repr__(self):
		return '<job_uuid {} skill_uuid {}>'.format(self.job_uuid, self.skill_uuid)
