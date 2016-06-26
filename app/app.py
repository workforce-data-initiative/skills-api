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

from api.v1_0 import api_bp as api_1_0_blueprint

# register api blueprints for versions
app.register_blueprint(api_1_0_blueprint, url_prefix='/v1.0')


