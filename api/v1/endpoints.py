# -*- coding: utf-8 -*-

"""API Version 1 Endpoints

This module contains all the implementation logic for the Version 1 API. 
In order to maintain consistency, it mirrors the endpoints module in the
router package.

Note:
    All classes in this module inherit from the Flask RESTful Resource parent
    class.

"""

import math
import json
from flask import abort, request
from flask_restful import Resource
from  common.utils import create_response, create_error
from . models.jobs_master import JobMaster
from . models.skills_master import SkillMaster
from . models.jobs_alternate_titles import JobAlternateTitle
from . models.jobs_unusual_titles import JobUnusualTitle
from . models.jobs_skills import JobSkill
from collections import OrderedDict

# Pagination Control Parameters
MAX_PAGINATION_LIMIT = 500
DEFAULT_PAGINATION_LIMIT = 20

# ------------------------------------------------------------------------
# Helper Methods 
# ------------------------------------------------------------------------
def compute_offset(page, items_per_page):
    """Calculate the offset value to use for pagination.

    Args:
        page (int): The current page to compute the offset from.
        items_per_page (int): Number of items per page.

    """
    return (page - 1) * items_per_page

def compute_page(offset, items_per_page):
    """Calculate the current page number based on offset.
    
    Args:
        offset (int): The offset to use for calculating the page.
        items_per_page (int): Number of items per page.

    """
    return int(math.ceil(offset / items_per_page)) + 1

def get_limit_and_offset(args):
    """Calculate the limit and offset to use for pagination
    
    Args:
        args (dict): All parameters passed in via the HTTP request.
    
    """
    limit = 0
    offset = 0
    if args is not None:
        if 'offset' in args.keys():
            try:
                offset = int(args['offset'])
                if offset < 0:
                    offset = 0                        
            except:
                offset = 0                 
        else:
            offset = 0

        if 'limit' in args.keys():
            try:
                limit = int(args['limit'])
                if limit < 0:
                    limit = DEFAULT_PAGINATION_LIMIT
            except:
                limit = DEFAULT_PAGINATION_LIMIT
        else:
            limit = DEFAULT_PAGINATION_LIMIT
    else:
        offset = 0
        limit = DEFAULT_PAGINATION_LIMIT
    
    if limit > MAX_PAGINATION_LIMIT:
        limit = MAX_PAGINATION_LIMIT

    return limit, offset

# ------------------------------------------------------------------------
# API Version 1 Endpoints 
# ------------------------------------------------------------------------
class AllJobsEndpoint(Resource):
    """All Jobs Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A collection of jobs.

        Notes:
            The endpoint supports pagination.

        """

        args = request.args
        limit, offset = get_limit_and_offset(args)

        all_jobs = []
        links = OrderedDict()
        links['links'] = []
        jobs = JobAlternateTitle.query.order_by(JobAlternateTitle.title.asc()).limit(limit).offset(offset)
        rows = JobAlternateTitle.query.count()

        # compute pages
        url_link = '/jobs?offset={}&limit={}'
        custom_headers = []
        custom_headers.append('X-Total-Count = ' + str(rows))

        total_pages = int(math.ceil(rows / limit))
        current_page = compute_page(offset, limit)
        first = OrderedDict()
        prev = OrderedDict()
        next = OrderedDict()
        last = OrderedDict()
        current = OrderedDict()

        current['rel'] = 'self'
        current['href'] = url_link.format(str(offset), str(limit))
        links['links'].append(current)
        
        first['rel'] = 'first'
        first['href'] = url_link.format(str(compute_offset(1, limit)), str(limit))
        links['links'].append(first)
        
        if current_page > 1:
            prev['rel'] = 'prev'
            prev['href'] = url_link.format(str(compute_offset(current_page - 1, limit)), str(limit))
            links['links'].append(prev)

        if current_page < total_pages:
            next['rel'] = 'next'
            next['href'] = url_link.format(str(compute_offset(current_page + 1, limit)), str(limit))
            links['links'].append(next)

        last['rel'] = 'last'
        last['href'] = url_link.format(str(compute_offset(total_pages, limit)), str(limit)) 
        links['links'].append(last)

        if jobs is not None:
            for job in jobs:
                job_response = OrderedDict()
                job_response['uuid'] = job.uuid
                job_response['title'] = job.title
                job_response['normalized_job_title'] = job.nlp_a
                job_response['parent_uuid'] = job.job_uuid
                all_jobs.append(job_response)
            
            all_jobs.append(links)
        
            return create_response(all_jobs, 200, custom_headers)
        else:
            return create_error('No jobs were found', 404)

class AllSkillsEndpoint(Resource):
    """All Skills Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A collection of skills.

        Notes:
            The endpoint supports pagination. 

        """
        args = request.args
        limit, offset = get_limit_and_offset(args)

        all_skills = []
        links = OrderedDict()
        links['links'] = []

        skills = SkillMaster.query.order_by(SkillMaster.skill_name.asc()).limit(limit).offset(offset)
        rows = SkillMaster.query.count()

        # compute pages
        url_link = '/skills?offset={}&limit={}'
        custom_headers = []
        custom_headers.append('X-Total-Count = ' + str(rows))

        total_pages = int(math.ceil(rows / limit))
        current_page = compute_page(offset, limit)
        first = OrderedDict()
        prev = OrderedDict()
        next = OrderedDict()
        last = OrderedDict()
        current = OrderedDict()

        current['rel'] = 'self'
        current['href'] = url_link.format(str(offset), str(limit))
        links['links'].append(current)
        
        first['rel'] = 'first'
        first['href'] = url_link.format(str(compute_offset(1, limit)), str(limit))
        links['links'].append(first)
        
        if current_page > 1:
            prev['rel'] = 'prev'
            prev['href'] = url_link.format(str(compute_offset(current_page - 1, limit)), str(limit))
            links['links'].append(prev)

        if current_page < total_pages:
            next['rel'] = 'next'
            next['href'] = url_link.format(str(compute_offset(current_page + 1, limit)), str(limit))
            links['links'].append(next)

        last['rel'] = 'last'
        last['href'] = url_link.format(str(compute_offset(total_pages, limit)), str(limit)) 
        links['links'].append(last)


        if skills is not None:
            for skill in skills:
                skill_response = OrderedDict()
                skill_response['uuid'] = skill.uuid
                skill_response['name'] = skill.skill_name
                skill_response['description'] = skill.description
                skill_response['onet_element_id'] = skill.onet_element_id
                skill_response['normalized_skill_name'] = skill.nlp_a
                all_skills.append(skill_response)
            all_skills.append(links)
        
            return create_response(all_skills, 200, custom_headers)
        else:
            return create_error('No skills were found', 404)

class JobTitleAutocompleteEndpoint(Resource):
    """Job Title Autocomplete Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A collection of jobs that partially match the specified search string.

        """
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
                return create_error('Invalid query mode specified for job title autocomplete', 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []

            if query_mode == 'begins_with':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.nlp_a.startswith(search_string.lower())).all()

            if query_mode == 'contains':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.nlp_a.contains(search_string.lower())).all()

            if query_mode == 'ends_with':
                results = JobAlternateTitle.query.filter(JobAlternateTitle.nlp_a.endswith(search_string.lower())).all()

            if len(results) == 0:
                return create_error('No job title suggestions found', 404)                

            for result in results:
                suggestion = OrderedDict()
                suggestion['uuid'] = result.uuid
                suggestion['suggestion'] = result.title
                suggestion['normalized_job_title'] = result.nlp_a
                suggestion['parent_uuid'] = result.job_uuid
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error('No job title suggestions found', 404)

class SkillNameAutocompleteEndpoint(Resource):
    """Skill Name Autocomplete Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A collection of skills that partially match the specified search string.

        """
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
                return create_error('Invalid query mode specified for skill name autocomplete', 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
           
            if query_mode == 'begins_with':
                results = SkillMaster.query.filter(SkillMaster.nlp_a.startswith(search_string.lower())).all()

            if query_mode == 'contains':
                results = SkillMaster.query.filter(SkillMaster.nlp_a.contains(search_string.lower())).all()

            if query_mode == 'ends_with':
                results = SkillMaster.query.filter(SkillMaster.nlp_a.endswith(search_string.lower())).all()

            if len(results) == 0:
                return create_error('No skill name suggestions found', 404)                

            for result in results:
                suggestion = OrderedDict()
                suggestion['uuid'] = result.uuid
                suggestion['suggestion'] = result.skill_name
                suggestion['normalized_skill_name'] = result.nlp_a
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error('No skill name suggestions found', 404)

class JobTitleNormalizeEndpoint(Resource):
    """Job Title Normalize Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A normalized version of a specified job title.

        """
        args = request.args
        
        if args is not None:
            if 'job_title' in args.keys():
                search_string = str(args['job_title'])
            else:
                return create_error('Invalid parameter specified for job title normalization', 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
            
            results = JobUnusualTitle.query.filter(JobUnusualTitle.title.contains(search_string.lower())).all()

            if len(results) == 0:
                return create_error('No normalized job titles found', 404)                

            for result in results:
                suggestion = OrderedDict()
                suggestion['uuid'] = result.uuid
                suggestion['title'] = result.title
                suggestion['description'] = result.description
                suggestion['parent_uuid'] = result.job_uuid
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error('No normalized job titles found', 404)    
            
class JobTitleFromONetCodeEndpoint(Resource):
    """Job Title From O*NET SOC Code Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            A job associated with its O*NET SOC code or UUID.

        Notes:
            This endpoint actually supports two use cases. It first checks if 
            the identifier is a valid O*NET SOC code, if not it queries for a 
            UUID.

        """
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
                    output['normalized_job_title'] = result.nlp_a
                    output['parent_uuid'] = result.job_uuid
                    return create_response(output, 200)
                else:
                    result = JobUnusualTitle.query.filter_by(uuid = id).first()
                    if result is not None:
                        output = OrderedDict()
                        output['uuid'] = result.uuid
                        output['title'] = result.title
                        output['normalized_job_title'] = result.title
                        output['parent_uuid'] = result.job_uuid
                        return create_response(output, 200)
                    else:
                        return create_error('Cannot find job with id ' + id, 404)
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
    """Normalize Skill Name Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A normalized version of a specified skill name.

        """
        args = request.args
        
        if args is not None:
            if 'skill_name' in args.keys():
                search_string = str(args['skill_name'])
            else:
                return create_error('Invalid parameter specified for skill name normalization', 400)

            search_string = search_string.replace('"','').strip()
            all_suggestions = []
            
            results = SkillMaster.query.filter(SkillMaster.skill_name.contains(search_string)).all()

            if len(results) == 0:
                return create_error('No normalized skill names found', 404)                

            for result in results:
                suggestion = OrderedDict()
                suggestion['uuid'] = result.uuid
                suggestion['skill_name'] = result.skill_name
                all_suggestions.append(suggestion)

            return create_response(all_suggestions, 200)
        else:
            return create_error('No normalized skill names found', 404) 

class AssociatedSkillsForJobEndpoint(Resource):
    """Associated Skills For Job Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            A collection of skills associated with a particular job UUID.

        """
        if id is not None:
            results = JobSkill.query.filter_by(job_uuid = id).all()
            job = JobMaster.query.filter_by(uuid = id).first()
            if not results:
                parent_uuid = None
                job = JobAlternateTitle.query.filter_by(uuid = id).first()
                if job:
                    parent_uuid = job.job_uuid
                else:
                    job = JobUnusualTitle.query.filter_by(uuid = id).first()
                    if job:
                        parent_uuid = job.job_uuid
                
                if parent_uuid is not None:
                    results = JobSkill.query.filter_by(job_uuid = parent_uuid).all()
                    
            if len(results) > 0:
                all_skills = OrderedDict()
                all_skills['job_uuid'] = id
                all_skills['job_title'] = job.title
                all_skills['normalized_job_title'] = job.nlp_a
                all_skills['skills'] = []
                for result in results:
                    skill = OrderedDict()
                    skill_desc = SkillMaster.query.filter_by(uuid = result.skill_uuid).first()
                    skill['skill_uuid'] = result.skill_uuid
                    skill['skill_name'] = skill_desc.skill_name
                    skill['description'] = skill_desc.description
                    skill['normalized_skill_name'] = skill_desc.nlp_a
                    all_skills['skills'].append(skill)
                return create_response(all_skills, 200)
            else:
                return create_error('No associated skills found for job ' + id, 404)
        else:
            return create_error('No job UUID specified for query', 400)

class AssociatedJobsForSkillEndpoint(Resource):
    """Associated Jobs For Skill Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            A collection of jobs associated with a specified skill UUID.

        """
        if id is not None:
            results = JobSkill.query.filter_by(skill_uuid = id).all()
            if len(results) > 0:
                all_jobs = OrderedDict()
                skill = SkillMaster.query.filter_by(uuid = id).first()
                all_jobs['skill_uuid'] = id
                all_jobs['skill_name'] = skill.skill_name
                all_jobs['normalized_skill_name'] = skill.nlp_a
                all_jobs['jobs'] = []
                for result in results:
                    job = OrderedDict()
                    job_desc = JobMaster.query.filter_by(uuid = result.job_uuid).first()
                    job['job_uuid'] = result.job_uuid
                    job['job_title'] = job_desc.title
                    job['normalized_job_title'] = job_desc.nlp_a
                    all_jobs['jobs'].append(job)
                return create_response(all_jobs, 200)
            else:
                return create_error('No associated jobs found for skill ' + id, 404)
        else:
            return create_error('No skill UUID specified for query', 400)

class AssociatedJobsForJobEndpoint(Resource):
    """Associated Jobs For Job Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            A collection of jobs associated with a specified job UUID.

        """
        if id is not None:
            parent_uuid = None
            result = JobMaster.query.filter_by(uuid = id).first()
            if result is None:
                result = JobAlternateTitle.query.filter_by(uuid = id).first()
                if result is None:
                    result = JobUnusualTitle.query.filter_by(uuid = id).first()
                    if result is not None:
                        parent_uuid = result.job_uuid
                    else:
                        return create_error('No job found matching the specified uuid ' + id, 404)
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
                title['parent_uuid'] = parent_uuid
                output['related_job_titles'].append(title)
                
            # unusual job titles
            other_titles = JobUnusualTitle.query.filter_by(job_uuid = parent_uuid).all()
            for other_title in other_titles:
                title = OrderedDict()
                title['uuid'] = other_title.uuid
                title['title'] = other_title.title
                title['parent_uuid'] = parent_uuid
                output['unusual_job_titles'].append(title)

            
            return create_response(output, 200)
        else:
            return create_error('No Job UUID specified for query', 400)

class AssociatedSkillForSkillEndpoint(Resource):
    """Associated Skill For Skills Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            A collection of skills associated with a specified skill UUID.

        """
        if id is not None:
            result = SkillMaster.query.filter_by(uuid = id).first()
            if result is not None:
                all_skills = OrderedDict()
                skills = SkillMaster.query.filter(SkillMaster.skill_name.contains(result.skill_name)).all()
                if len(skills) > 0:
                    all_skills['skills'] = []
                    for skill in skills:
                        output = OrderedDict()
                        output['uuid'] = skill.uuid
                        output['skill_name'] = skill.skill_name
                        output['normalized_skill_name'] = skill.nlp_a
                        all_skills['skills'].append(output)
                    return create_response(all_skills, 200)
            else:
                return create_error('Cannot find skills associated with id ' + id, 404)
        else:
            return create_error('No skill UUID specified for query', 400)

class SkillNameAndFrequencyEndpoint(Resource):
    """Skill Name And Frequency Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Returns: 
            The name and frequency of all skills.

        """
        if id is not None:
            result = SkillMaster.query.filter_by(uuid = id).first()
            if result is None:
                all_skills = OrderedDict()
                job = JobMaster.query.filter_by(onet_soc_code = id).first()
                if job is not None:
                    search_uuid = job.uuid
                else:
                    return create_error('Cannot find skills associated with id ' + id, 404)
                
                results = JobSkill.query.filter_by(job_uuid = search_uuid).all()
                if len(results) == 0:
                    return create_error('Cannot find skills associated with id ' + id, 404)
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
                output['description'] = result.description
                output['normalized_skill_name'] = result.nlp_a
              
                return create_response(output, 200)

class AllUnusualJobsEndpoint(Resource):
    """All Unusual Jobs Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A collection of job titles that fall outside the standard titles used for particular jobs.

        """
        all_jobs = []
        jobs = JobUnusualTitle.query.order_by(JobUnusualTitle.title.asc()).all()
        if jobs is not None:
            for job in jobs:
                job_response = OrderedDict()
                job_response['uuid'] = job.uuid
                job_response['title'] = job.title
                job_response['description'] = job.description
                job_response['job_uuid'] = job.job_uuid
                all_jobs.append(job_response)
        
            return create_response(all_jobs, 200)
        else:
            return create_error('No jobs were found', 404)
