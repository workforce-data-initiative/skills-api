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

from api.jobs import Job
from api.skills import Skill

api.add_resource(Job, '/jobs/<int:id>')
api.add_resource(Skill, '/skills/<int:id>')
