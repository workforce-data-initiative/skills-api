# -*- coding: utf-8 -*-

""" OpenSkills API application.

This package is the main entryway to the API. It provides all the configuration
elements needed to run the application.

"""

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_cors import CORS, cross_origin

# ----------------------------------------------------------------------------
# Flask Application Configuration
# ----------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object('config.config.Config')
CORS(app)

# ----------------------------------------------------------------------------
# Flask-RESTFul API Object
# ----------------------------------------------------------------------------
api = Api(app, catch_all_404s=True)

# ----------------------------------------------------------------------------
# Database
# ----------------------------------------------------------------------------
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.router import api_bp as api_router_blueprint
from api.v1 import api_bp as api_1_blueprint

# ----------------------------------------------------------------------------
# API Blueprints
# ----------------------------------------------------------------------------
app.register_blueprint(api_router_blueprint)
app.register_blueprint(api_1_blueprint, url_prefix='/v1')

