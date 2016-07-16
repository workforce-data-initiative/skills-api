# -*- coding: utf-8 -*-

"""
api.v1_0.endpoints
~~~~~~~~~~~~~~~~~~

"""

from flask import abort, request
from flask_restful import Resource
from flask_restful_swagger import swagger
from  common.utils import create_response, create_error 
from . models.jobs_master import JobMaster
from . models.skills_master import SkillMaster
from . models.jobs_alternate_titles import JobAlternateTitle
from . models.jobs_unusual_titles import JobUnusualTitle
from . models.jobs_skills import JobSkill
from collections import OrderedDict

class AllJobsEndpoint(Resource):
    @swagger.operation(
        description = "Retrieve All Jobs",
        summary = "Retrieves the names and UUIDs of all jobs.",
        notes = "The job collection is huge and may take a while before the API call returns the full dataset.",
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of job titles."
            },
            {
                "code" : 404,
                "message" : "Unable to find any job titles."
            }
        ]
    )
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
    @swagger.operation(
        description = "Retrieve All Skills",
        summary = "Retrieves the names and UUIDs of all skills.",
        notes = "The skill collection is huge and may take a while before the API call returns the full dataset.",
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of skills."
            },
            {
                "code" : 404,
                "message" : "Unable to find any skills."
            }
        ]
    )
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
    @swagger.operation(
        description = "Job Title Autocomplete",
        summary = "Allows autocompletion of a job title as a user is typing.",
        notes = "Append the parameters, begins_with, contains, and ends_with to the request URL",
        parameters = [
            {
                "name": "begins_with",
                "paramType": "query",
                "description": "Find job titles beginning with the specified text fragment",
                "required": False,
                "type": "string"
            },
            {
                "name": "contains",
                "paramType": "query",
                "description": "Find job titles containing the specified text fragment",
                "required": False,
                "type": "string"
            },
            {
                "name": "ends_with",
                "paramType": "query",
                "description": "Find job titles ending with the specified text fragment",
                "required": False,
                "type": "string"
            }
        ],        
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of job titles matching the given string."
            },
            {
                "code" : 400,
                "message" : "Bad request (i.e. forgotten to specify a parameter or incorrect parameter provided.)"
            },
            {
                "code" : 404,
                "message" : "Unable to find any job titles that match the given string."
            }
        ]
    )
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
                return create_error({'message': 'Invalid query mode specified for job title autocomplete'}, 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
           
            if query_mode == 'begins_with':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.title.startswith(search_string)).all()

            if query_mode == 'contains':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.title.contains(search_string)).all()

            if query_mode == 'ends_with':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.title.endswith(search_string)).all()

            if len(results) == 0:
                return create_error({'message': 'No job title suggestions found'}, 404)                

            for result in results:
                suggestion = {}
                suggestion['suggestion'] = result.title
                suggestion['uuid'] = result.uuid
                suggestion['parent_uuid'] = result.job_uuid
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error({'message': 'No job title suggestions found'}, 404)

class SkillNameAutocompleteEndpoint(Resource):
    @swagger.operation(
        description = "Job Title Autocomplete",
        summary = "Allows autocompletion of a skill name as a user is typing.",
        notes = "Append the parameters, begins_with, contains, and ends_with to the request URL",
        parameters = [
            {
                "name": "begins_with",
                "paramType": "query",
                "description": "Find skill names beginning with the specified text fragment",
                "required": False,
                "type": "string"
            },
            {
                "name": "contains",
                "paramType": "query",
                "description": "Find skill names containing the specified text fragment",
                "required": False,
                "type": "string"
            },
            {
                "name": "ends_with",
                "paramType": "query",
                "description": "Find skill names ending with the specified text fragment",
                "required": False,
                "type": "string"
            }
        ],        
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of skill names matching the given string."
            },
            {
                "code" : 400,
                "message" : "Bad request (i.e. forgotten to specify a parameter or incorrect parameter provided.)"
            },
            {
                "code" : 404,
                "message" : "Unable to find any skill names that match the given string."
            }
        ]
    )
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
                return create_error({'message': 'Invalid query mode specified for skill name autocomplete'}, 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
           
            if query_mode == 'begins_with':
                results = SkillMaster.query.filter(SkillMaster.skill_name.startswith(search_string)).all()

            if query_mode == 'contains':
                results = SkillMaster.query.filter(SkillMaster.skill_name.contains(search_string)).all()

            if query_mode == 'ends_with':
                results = SkillMaster.query.filter(SkillMaster.skill_name.endswith(search_string)).all()

            if len(results) == 0:
                return create_error({'message': 'No skill name suggestions found'}, 404)                

            for result in results:
                suggestion = {}
                suggestion['suggestion'] = result.skill_name
                suggestion['uuid'] = result.uuid
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error({'message': 'No skill name suggestions found'}, 404)

class JobTitleNormalizeEndpoint(Resource):
    @swagger.operation(
        description = "Normalize Job Title",
        summary = "Find the canonical job title (like \"Baker\") for an entered synonymous job title (like \"Cupcake ninja\")",
        notes = "Append the parameter title to the request URL (may be a partial or complete job title).",
        parameters = [
            {
                "name": "job_title",
                "paramType": "query",
                "description": "Find job titles matching the specified title (or text fragment)",
                "required": True,
                "type": "string"
            }
        ],        
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of job titles matching the given string."
            },
            {
                "code" : 400,
                "message" : "Bad request (i.e. forgotten to specify a parameter or incorrect parameter provided.)"
            },
            {
                "code" : 404,
                "message" : "Unable to find any job titles that match the given string."
            }
        ]
    )
    def get(self):
        args = request.args
        
        if args is not None:
            if 'job_title' in args.keys():
                search_string = str(args['job_title'])
            else:
                return create_error({'message': 'Invalid parameter specified for job title normalization'}, 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
            
            results = JobUnusualTitle.query.filter(JobUnusualTitle.title.contains(search_string)).all()

            if len(results) == 0:
                return create_error({'message': 'No normalized job titles found'}, 404)                

            for result in results:
                suggestion = {}
                suggestion['title'] = result.title
                suggestion['uuid'] = result.uuid
                suggestion['parent_uuid'] = result.job_uuid
                suggestion['description'] = result.description
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error({'message': 'No normalized job titles found'}, 404)    
            
class JobTitleFromONetCodeEndpoint(Resource):
    @swagger.operation(
    )
    def get(self, id=None):
        if id is not None:
            result = JobMaster.query.filter_by(onet_soc_code = id).first()
            if result is None:
                result = JobMaster.query.filter_by(uuid = id).first()

            if result is None:
                # search for a related job
                result = JobAlternateTitle.query.filter_by(uuid = id).first()
                if result is not None:
                    output = OrderedDict()
                    output['uuid'] = result.uuid
                    output['title'] = result.title
                    output['parent_uuid'] = result.job_uuid
                    return create_response(output, 200)
                else:
                    result = JobUnusualTitle.query.filter_by(uuid = id).first()
                    if result is not None:
                        output = OrderedDict()
                        output['uuid'] = result.uuid
                        output['title'] = result.title
                        output['description'] = result.description
                        output['parent_uuid'] = result.job_uuid
                        return create_response(output, 200)
                    else:
                        return create_error({'message':'Cannot find job with id ' + id}, 404)
            else:
                output = OrderedDict()
                output['uuid'] = result.uuid
                output['onet_soc_code'] = result.onet_soc_code
                output['title'] = result.title
                output['description'] = result.description
                output['related_job_titles'] = []
                output['unusual_job_titles'] = []
                
                # alternate job titles
                alt_titles = JobAlternateTitle.query.filter_by(job_uuid = result.uuid).all()
                for alt_title in alt_titles:
                    title = OrderedDict()
                    title['uuid'] = alt_title.uuid
                    title['title'] = alt_title.title
                    output['related_job_titles'].append(title)
                
                # unusual job titles
                other_titles = JobUnusualTitle.query.filter_by(job_uuid = result.uuid).all()
                for other_title in other_titles:
                    title = OrderedDict()
                    title['uuid'] = other_title.uuid
                    title['title'] = other_title.title
                    output['unusual_job_titles'].append(title)
                
                
                return create_response(output, 200)


class NormalizeSkillNameEndpoint(Resource):
    @swagger.operation(
        description = "Normalize Skill Name",
        summary = "Find the canonical skill name (like “Ruby programming”) for an entered synonymous skill name (like “Coding in Ruby”)",
        notes = "Append the parameter skill_name to the request URL (may be a partial or complete skill name).",
        parameters = [
            {
                "name": "skill_name",
                "paramType": "query",
                "description": "Find skill names matching the specified title (or text fragment)",
                "required": True,
                "type": "string"
            }
        ],        
        responseMessages = [
            {
                "code" : 200,
                "message" : "Successfully found a collection of skill names matching the given string."
            },
            {
                "code" : 400,
                "message" : "Bad request (i.e. forgotten to specify a parameter or incorrect parameter provided.)"
            },
            {
                "code" : 404,
                "message" : "Unable to find any skill names that match the given string."
            }
        ]
    )
    def get(self):
        args = request.args
        
        if args is not None:
            if 'skill_name' in args.keys():
                search_string = str(args['skill_name'])
            else:
                return create_error({'message': 'Invalid parameter specified for skill name normalization'}, 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
            
            results = SkillMaster.query.filter(SkillMaster.skill_name.contains(search_string)).all()

            if len(results) == 0:
                return create_error({'message': 'No normalized skill names found'}, 404)                

            for result in results:
                suggestion = {}
                suggestion['skill_name'] = result.skill_name
                suggestion['uuid'] = result.uuid
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error({'message': 'No normalized skill names found'}, 404) 

class AssociatedSkillsForJobEndpoint(Resource):
    @swagger.operation(
    )
    def get(self, id=None):
        if id is not None:
            results = JobSkill.query.filter_by(job_uuid = id).all()
            if len(results) > 0:
                all_skills = {}
                all_skills['job_uuid'] = id
                all_skills['skills'] = []
                for result in results:
                    skill ={}
                    skill['skill_uuid'] = result.skill_uuid
                    all_skills['skills'].append(skill)
                return create_response(all_skills, 200)
            else:
                return create_error({'message': 'No associated skills found for job ' + id}, 404)
        else:
            return create_error({'message': 'No job UUID specified for query'}, 400)

class AssociatedJobsForSkillEndpoint(Resource):
    @swagger.operation(

    )
    def get(self, id=None):
        if id is not None:
            results = JobSkill.query.filter_by(skill_uuid = id).all()
            if len(results) > 0:
                all_jobs = {}
                all_jobs['skill_uuid'] = id
                all_jobs['jobs'] = []
                for result in results:
                    job ={}
                    job['job_uuid'] = result.job_uuid
                    all_jobs['jobs'].append(job)
                return create_response(all_jobs, 200)
            else:
                return create_error({'message': 'No associated jobs found for skill ' + id}, 404)
        else:
            return create_error({'message': 'No skill UUID specified for query'}, 400)

class AssociatedJobsForJobEndpoint(Resource):
    @swagger.operation(
    )
    def get(self, id=None):
        if id is not None:
            parent_uuid = None
            result = JobMaster.query.filter_by(uuid = id).first()
            if result is None:
                result = JobAlternateTitle.query.filter_by(uuid = id).first()
                if result is None:
                    result = JobUnusualTitle.query.filter_by(uuid = id).first()
                    if result is None:
                        parent_uuid = result.job_id
                    else:
                        return create_error({'message': 'No job found matching the specified uuid ' + id}, 404)
                else:
                    parent_uuid = result.job_uuid
            else:
                parent_uuid = result.uuid
    
            output = OrderedDict()
            output['related_job_titles'] = []
            output['unusual_job_titles'] = []
                
            # alternate job titles
            alt_titles = JobAlternateTitle.query.filter_by(job_uuid = parent_uuid).all()
            for alt_title in alt_titles:
                title = OrderedDict()
                title['uuid'] = alt_title.uuid
                title['title'] = alt_title.title
                output['related_job_titles'].append(title)
                
            # unusual job titles
            other_titles = JobUnusualTitle.query.filter_by(job_uuid = parent_uuid).all()
            for other_title in other_titles:
                title = OrderedDict()
                title['uuid'] = other_title.uuid
                title['title'] = other_title.title
                output['unusual_job_titles'].append(title)

            
            return create_response(output, 200)
        else:
            return create_error({'message': 'No Job UUID specified for query'}, 400)

class AssociatedSkillForSkillEndpoint(Resource):
    @swagger.operation(
    )
    def get(self, id=None):
        if id is not None:
            result = SkillMaster.query.filter_by(uuid = id).first()
            if result is not None:
                all_skills = {}
                skills = SkillMaster.query.filter(SkillMaster.skill_name.contains(result.skill_name)).all()
                if len(skills) > 0:
                    all_skills['skills'] = []
                    for skill in skills:
                        output = OrderedDict()
                        output['skill_uuid'] = skill.uuid
                        output['skill_name'] = skill.skill_name
                        all_skills['skills'].append(output)
                    return create_response(all_skills, 200)
            else:
                return create_error({'message':'Cannot find skills associated with id ' + id}, 404)
        else:
            return create_error({'message': 'No skill UUID specified for query'}, 400)

class SkillNameAndFrequencyEndpoint(Resource):
    @swagger.operation(
    )
    def get(self, id=None):
        if id is not None:
            result = SkillMaster.query.filter_by(uuid = id).first()
            if result is None:
                all_skills = {}
                job = JobMaster.query.filter_by(onet_soc_code = id).first()
                if job is not None:
                    search_uuid = job.uuid
                else:
                    return create_error({'message':'Cannot find skills associated with id ' + id}, 404)
                
                results = JobSkill.query.filter_by(job_uuid = search_uuid).all()
                if len(results) == 0:
                    return create_error({'message':'Cannot find skills associated with id ' + id}, 404)
                else:
                    all_skills['onet_soc_code'] = id
                    all_skills['job_uuid'] = search_uuid
                    all_skills['title'] = job.title
                    all_skills['skills'] = []
                    for result in results: 
                        output = OrderedDict()
                        output['skill_uuid'] = result.skill_uuid
                        all_skills['skills'].append(output)
              
                    return create_response(all_skills, 200)
            else:
                output = OrderedDict()
                output['uuid'] = result.uuid
                output['skill_name'] = result.skill_name
                output['count'] = result.count
              
                return create_response(output, 200)