# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from flask_restful import Api

app = Flask(__name__)
app.config.from_object('api_config.config.Config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills
from db.models.job_skills import JobSkills

from api.jobs import JobSkill
from api.skills import Skill
from api.skills import ONETSkill

api.add_resource(JobSkill, '/jobs/<string:id>/skills')
api.add_resource(Skill, '/skills/<string:id>', '/skills')
api.add_resource(ONETSkill, '/skills/<string:id>/uuid')
