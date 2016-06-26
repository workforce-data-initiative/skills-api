# -*- coding: utf-8 -*-

"""
app.app
~~~~~~~

OpenSkills API application root.

"""

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('config.config.Config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


