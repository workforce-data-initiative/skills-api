# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from api.resources.skills import Skill
from api.resources.jobs import Job
from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills

app = Flask(__name__)
app.config.from_object('api_config.config.Config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# API endpoints
api.add_resource(Skill, '/skills')
api.add_resource(Job, '/jobs')
