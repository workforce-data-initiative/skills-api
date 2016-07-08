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


from db.models.skills_master import SkillMaster
from db.models.related_skills import RelatedSkill
from db.models.job_skills import JobSkill
from db.models.jobs import Job
from db.models.jobs import AlternateJobTitle

from api.jobs import JobSkillEndpoint
from api.skills import SkillEndpoint
from api.skills import ONETSkillEndpoint
from api.skills import SkillAutocompleteEndpoint
from api.jobs import JobEndpoint
from api.jobs import JobAutocompleteEndpoint

api.add_resource(JobSkillEndpoint, '/jobs/<string:id>/skills')
api.add_resource(SkillEndpoint, '/skills/<string:id>', '/skills')
api.add_resource(ONETSkillEndpoint, '/skills/<string:id>/uuids')
api.add_resource(JobEndpoint, '/jobs/<string:id>', '/jobs', endpoint='job_ep')
api.add_resource(SkillAutocompleteEndpoint, '/skills/autocomplete', \
        endpoint='skills_autocomplete')
api.add_resource(JobAutocompleteEndpoint, '/jobs/autocomplete', \
        endpoint='jobs_autocomplete')
