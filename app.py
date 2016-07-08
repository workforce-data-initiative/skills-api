# -*- coding: utf-8 -*-

"""
app.py
~~~~~~
Management application for the Open Data API.
"""

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api.resources.skills import Skill
from api.resources.jobs import Job
from db.models.skills_master import SkillsMaster
from db.models.related_skills import RelatedSkills

app = Flask(__name__)

# TODO - Move this to a configuration object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Decorate the Flask application with all the necessary extensions
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

# Add the SQLAlchemy database utilities to the manager utility
manager.add_command('db', MigrateCommand)

# API endpoints
api.add_resource(Skill, '/skills')
api.add_resource(Job, '/jobs')

if __name__ == '__main__':
    manager.run()