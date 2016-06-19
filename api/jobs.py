# -*- coding: utf-8 -*-

"""
api.jobs
~~~~~~~~~
Definitions of all methods associated with jobs endpoints.
"""

from flask import abort
from flask_restful import Resource
from collections import OrderedDict
from app.app import db
from db.models.job_skills import JobSkill
from db.models.jobs import Job
from db.models.jobs import AlternateJobTitle

class JobEndpoint(Resource):
    def get(self, id=None):
        if id is not None:
            result = Job.query.filter_by(onet_soc_code = id).first()
            if result is None:
                result = Job.query.filter_by(uuid = id).first()

            if result is None:
                abort(404)
            else:
                output = OrderedDict()
                output['uuid'] = result.uuid
                output['onet_soc_code'] = result.onet_soc_code
                output['title'] = result.title
                output['description'] = result.description
                output['related_job_titles'] = []
                
                # alternate job titles
                alt_titles = AlternateJobTitle.query.filter_by(job_uuid = result.uuid).all()
                for alt_title in alt_titles:
                    title = OrderedDict()
                    title['uuid'] = alt_title.uuid
                    title['title'] = alt_title.title
                    output['related_job_titles'].append(title)
                return output
                
        else:
            results = Job.query.all()
            if results is not None:
                all_jobs = []
                for result in results:
                    output = OrderedDict()
                    output['uuid'] = result.uuid
                    output['onet_soc_code'] = result.onet_soc_code
                    output['title'] = result.title
                    output['description'] = result.description
                    all_jobs.append(output)
                return all_jobs
            else:
                abort(404)


class JobSkillEndpoint(Resource):
    def get(self, id):
        output = OrderedDict()
        result = JobSkill.query.filter_by(onet_soc_code = id).first()
        if result:
            return result.related_skills
        else:
            abort(404)
