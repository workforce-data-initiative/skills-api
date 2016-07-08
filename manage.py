# -*- coding: utf-8 -*-

"""
app.py
~~~~~~
Management application for the Open Data API.
"""

import os

from app.app import app, db
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)

import uuid

from db.models.skills_master import SkillsMaster
from db.models.job_skills import JobSkills

# Add the SQLAlchemy database utilities to the manager utility
manager.add_command('db', MigrateCommand)

@manager.command
def seed_skills_master():
    "Populate the skills_master database tables."
    with open(os.path.join('common', 'skills_master.tsv'), 'r') as f:
        lines = f.readlines()

    # dump the header
    lines = lines[1:]

    # collect unique skills from list of skills
    visited_skills = []
    count = 0

    for line in lines:
        line = line.strip().split('\t')
        if str(line[4]) not in visited_skills:
            skill_uuid = str(uuid.uuid4())
            onet_soc_code = str(line[2])
            onet_element_id = str(line[3])
            skill_name = str(line[4])
            skill_count = int(line[5])

            if (SkillsMaster.query.filter_by(skill_name = skill_name).count() == 0):
                skills_master = SkillsMaster(skill_uuid, onet_soc_code, \
                        onet_element_id, skill_name, skill_count)

                print 'Adding skill ' + skill_name
        
                try:
                    db.session.add(skills_master)
                    db.session.commit()
                    count += 1
                    visited_skills.append(skill_name)
                except:
                    print '\t-----> Could not add skill ' + skills_master.skill_name
            else:
                print 'Skipping ' + skill_name
                visited_skills.append(skill_name)

@manager.command
def seed_job_to_skills():
    "Populate the job_skills database tables."
    with open(os.path.join('common', 'job2skill_column_skill_index.tsv'), 'r') as f:
        lines = f.readlines()

    jobs = {}

    # dump the header
    lines = lines[1:]
    
    for line in lines:
        line = line.strip().split('\t')
        print 'Adding item ' + line[3]
        
        job_skill = dict([('skill_name', line[5]), ('count', line[6])])

        if line[3] not in jobs:
            jobs[line[3]] = []
        
        jobs[line[3]].append(job_skill.copy())

    for job in jobs:
        job_skill = JobSkills(job, jobs[job])
        try:
            db.session.add(job_skill)
            db.session.commit()
        except:
            print 'Could not add item ' + line[0]


if __name__ == '__main__':
    manager.run()
