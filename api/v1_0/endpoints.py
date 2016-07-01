# -*- coding: utf-8 -*-

"""
api.v1_0.endpoints
~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request
from flask_restful import Resource
from  common.utils import create_response, create_error 
from . models.jobs_master import JobMaster
from . models.skills_master import SkillMaster
from collections import OrderedDict

class AllJobsEndpoint(Resource):
    def get(self):
        all_jobs = []
        jobs = JobMaster.query.order_by(JobMaster.title.asc()).all()
        if jobs is not None:
            for job in jobs:
                job_response = OrderedDict()
                job_response['uuid'] = job.uuid
                job_response['onet_soc_code'] = job.onet_soc_code
                job_response['title'] = job.title
                job_response['description'] = job.description
                all_jobs.append(job_response)
        
            return create_response(all_jobs, 200)
        else:
            return create_error({'message':'No jobs were found'}, 404)

class AllSkillsEndpoint(Resource):
    def get(self):
        all_skills = []
        skills = SkillMaster.query.order_by(SkillMaster.count.desc()).all()
        if skills is not None:
            for skill in skills:
                skill_response = OrderedDict()
                skill_response['uuid'] = skill.uuid
                skill_response['name'] = skill.skill_name
                skill_response['count'] = skill.count
                all_skills.append(skill_response)
        
            return create_response(all_skills, 200)
        else:
            return create_error({'message':'No skills were found'}, 404)

class JobTitleAutocompleteEndpoint(Resource):
    def get(self):
        return create_response({'foo':'bar'}, 200)

class JobTitleNormalizeEndpoint(Resource):
    def get(self):
        return "endpoint 2"

class JobTitleFromONetCodeEndpoint(Resource):
    def get(self):
        return "endpoint 3"

class SkillNameAutocompleteEndpoint(Resource):
    def get(self):
        return "endpoint 4"

class NormalizeSkillNameEndpoint(Resource):
    def get(self):
        return "endpoint 5"

class NormalizedSkillUUIDFromONetCodeEndpoint(Resource):
    def get(self):
        return "endpoint 6"

class AssociatedSkillsForJobEndpoint(Resource):
    def get(self):
        return "endpoint 7"

class AssociatedJobsForJobEndpoint(Resource):
    def get(self):
        return "endpoint 8"

class AssociatedSkillForSkillEndpoint(Resource):
    def get(self):
        return "endpoint 9"

class SkillNameAndFrequencyEndpoint(Resource):
    def get(self):
        return "endpoint 10"

class JobNameFromUUIDEndpoint(Resource):
    def get(self):
        return "endpoint 11"

