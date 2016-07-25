# -*- coding: utf-8 -*-

"""
app.app
~~~~~~~

OpenSkills API application.

"""

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object('config.config.Config')
CORS(app)

api = Api(app, catch_all_404s=True)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.router import api_bp as api_router_blueprint
from api.v1 import api_bp as api_1_blueprint

# register api blueprints for versions
app.register_blueprint(api_router_blueprint)
app.register_blueprint(api_1_blueprint, url_prefix='/v1')

