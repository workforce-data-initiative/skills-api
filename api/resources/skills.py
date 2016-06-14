# -*- coding: utf-8 -*-

"""
api.resources.skills
~~~~~~~~~~~~~~~~~~~~
Definitions of all methods associated with skills endpoints.
"""

from flask_restful import Resource

class Skill(Resource):
    def get(self):
        return 'I am pretty darn skillful'