# -*- coding: utf-8 -*-

"""
api.skills
~~~~~~~~~~
Definitions of all methods associated with skills endpoints.
"""

from flask import abort
from flask_restful import Resource
from app.app import db
from db.models.skills_master import SkillMaster
from db.models.related_skills import RelatedSkill

import json

class ONETSkill(Resource):
    def get(self, id):
        if id is not None:
            output_array = []
            result = SkillMaster.query.filter_by(onet_soc_code = id).all()
            if result is not None:
                for res in result:
                    output = {}
                    output['skill_uuid'] = res.skill_uuid
                    output['onet_soc_code'] = res.onet_soc_code
                    output['onet_element_id'] = res.onet_element_id
                    output['skill_name'] = res.skill_name
                    output_array.append(output)
                return output_array
        else:
            abort(404)

class Skill(Resource):
    def get(self, id=None):
        if id is not None:
            output = {}
            result = SkillMaster.query.filter_by(skill_uuid = id).first()
            if result is not None:
                output['skill_uuid'] = result.skill_uuid
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
                    output = {}
                    output['skill_uuid'] = res.skill_uuid
                    output['skill_name'] = res.skill_name
                    output['count'] = res.count
                    output_array.append(output)
                return output_array
            else:
                abort(404)

