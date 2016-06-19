# -*- coding: utf-8 -*-

"""
api.skills
~~~~~~~~~~
Definitions of all methods associated with skills endpoints.
"""

from flask import abort, request
from flask_restful import Resource
from collections import OrderedDict
from app.app import db
from db.models.skills_master import SkillMaster
from db.models.related_skills import RelatedSkill

class SkillAutocompleteEndpoint(Resource):
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
                results = SkillMaster.query.filter(SkillMaster.skill_name.startswith(search_string)).all()

            if query_mode == 'contains':
                results = SkillMaster.query.filter(SkillMaster.skill_name.contains(search_string)).all()

            if query_mode == 'ends_with':
                results = SkillMaster.query.filter(SkillMaster.skill_name.endswith(search_string)).all()

            for result in results:
                suggestion = {}
                suggestion['suggestion'] = result.skill_name
                all_suggestions.append(suggestion)

            return all_suggestions
        else:
            abort(400)

class ONETSkillEndpoint(Resource):
    def get(self, id):
        if id is not None:
            output_array = []
            result = SkillMaster.query.filter_by(onet_soc_code = id).all()
            if result is not None:
                for res in result:
                    output = OrderedDict()
                    output['uuid'] = res.uuid
                    output['onet_soc_code'] = res.onet_soc_code
                    output['onet_element_id'] = res.onet_element_id
                    output['skill_name'] = res.skill_name
                    output_array.append(output)
                return output_array
        else:
            abort(404)

class SkillEndpoint(Resource):
    def get(self, id=None):
        if id is not None:
            output = OrderedDict()
            result = SkillMaster.query.filter_by(uuid = id).first()
            if result is not None:
                output['uuid'] = result.uuid
                output['skill_name'] = result.skill_name
                output['count'] = result.count
                return output
            else:
                abort(404)
        else:
            output_array = []
            result = SkillMaster.query.order_by(SkillMaster.count.desc()).all()
            if result is not None:
                for res in result:
                    output = OrderedDict()
                    output['uuid'] = res.uuid
                    output['skill_name'] = res.skill_name
                    output['count'] = res.count
                    output_array.append(output)
                return output_array
            else:
                abort(404)
