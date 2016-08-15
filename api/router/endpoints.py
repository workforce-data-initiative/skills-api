# -*- coding: utf-8 -*-

"""API Façade.

The API façade provides routing for the API endpoints based on the version 
specified by the user either via a custom or Accept header.

Note:
    All classes in this module inherit from the Flask RESTful Resource parent
    class.

"""

from flask import abort, request, redirect, url_for
from flask_restful import Resource
from common.utils import route_api

# ------------------------------------------------------------------------
# API Version 1 Endpoints 
# ------------------------------------------------------------------------
class AllJobsEndpoint(Resource):
    """All Jobs Endpoint Class"""
    
    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('alljobsendpoint')

class AllSkillsEndpoint(Resource):
    """All Skills Endpoint Class"""
    
    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('allskillsendpoint')

class JobTitleAutocompleteEndpoint(Resource):
    """Job Title Autocomplete Endpoint Class"""
    
    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('jobtitleautocompleteendpoint')

class SkillNameAutocompleteEndpoint(Resource):
    """Skill Name Autocomplete Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('skillnameautocompleteendpoint')

class JobTitleNormalizeEndpoint(Resource):
    """Job Title Normalize Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('jobtitlenormalizeendpoint')


class AllUnusualJobsEndpoint(Resource):
    """All Unusual Jobs Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('allunusualjobsendpoint')

class JobTitleFromONetCodeEndpoint(Resource):
    """Job Title From O*NET SOC Code Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Args:
            id: Optional O*NET SOC Code to query for. All job titles if none
            specified. 

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('jobtitlefromonetcodeendpoint', id=id)

class NormalizeSkillNameEndpoint(Resource):
    """Normalize Skill Name Endpoint Class"""

    def get(self):
        """GET operation for the endpoint class.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('normalizeskillnameendpoint')

class AssociatedSkillsForJobEndpoint(Resource):
    """Associated Skills For Jobs Endpoint Class"""

    def get(self, id):
        """GET operation for the endpoint class.

        Args:
            id: Job UUID.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('associatedskillsforjobendpoint', id=id)
        
class AssociatedJobsForSkillEndpoint(Resource):
    """Associated Jobs For Skills Endpoint Class"""

    def get(self, id):
        """GET operation for the endpoint class.

        Args:
            id: Skill UUID.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('associatedjobsforskillendpoint', id=id)

class AssociatedJobsForJobEndpoint(Resource):
    """Associated Jobs For Job Endpoint Class"""

    def get(self, id=None):
        """GET operation for the endpoint class.

        Args:
            id: Optional job UUID.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('associatedjobsforjobendpoint', id=id)

class AssociatedSkillForSkillEndpoint(Resource):
    """Associated Skills For Skill Endpoint Class"""
    
    def get(self, id=None):
        """GET operation for the endpoint class.

        Args:
            id: Optional skill UUID.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('associatedskillforskillendpoint', id=id)

class SkillNameAndFrequencyEndpoint(Resource):
    """Skill Name And Frequency Endpoint Class"""
    
    def get(self, id=None):
        """GET operation for the endpoint class.

        Args:
            id: Optional skill UUID.

        Returns: 
            A redirect to the appropriate API version as specified by the 
            accept or custom header.

        """
        return route_api('skillnameandfrequencyendpoint', id=id)