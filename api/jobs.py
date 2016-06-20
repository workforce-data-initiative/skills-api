# -*- coding: utf-8 -*-

"""
api.jobs
~~~~~~~~~
Definitions of all methods associated with jobs endpoints.
"""

from flask import abort, request
from flask_restful import Resource
from collections import OrderedDict
from app.app import db
from db.models.job_skills import JobSkill
from db.models.jobs import Job
from db.models.jobs import AlternateJobTitle

class JobAutocompleteEndpoint(Resource):
    def get(self):
        args = request.args
        query_mode = ''
        if args is not None:
            if 'begins_with' in args.keys():
                search_string = str(args['begins_with'])
                query_mode = 'begins_with'
            elif 'contains' in args.keys():
                search_string = str(args['contains'])
                query_mode = 'contains'
            elif 'ends_with' in args.keys():
                search_string = str(args['ends_with'])
                query_mode = 'ends_with'
            else:
                abort(400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
           
            if query_mode == 'begins_with':
                results = AlternateJobTitle.query.filter(AlternateJobTitle.title.startswith(search_string)).all()

            if query_mode == 'contains':
                results = AlternateJobTitle.query.filter(AlternateJobTitle.title.contains(search_string)).all()

            if query_mode == 'ends_with':
                results = AlternateJobTitle.query.filter(AlternateJobTitle.title.endswith(search_string)).all()

            for result in results:
                suggestion = {}
                suggestion['suggestion'] = result.title
                all_suggestions.append(suggestion)

            return all_suggestions
        else:
            abort(400)

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
