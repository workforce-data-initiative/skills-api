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

from db.models.skills_master import SkillsMaster
from db.models.job_skills import JobSkills

# Add the SQLAlchemy database utilities to the manager utility
manager.add_command('db', MigrateCommand)

@manager.command
def seed_skills_master():
    "Populate the skills_master database tables."
    with open(os.path.join('common', 'skills_master.csv'), 'r') as f:
        lines = f.readlines()

    # dump the header
    lines = lines[1:]
    
    for line in lines:
        line = line.strip().split(',')[1:]
        skills_master = SkillsMaster(line[0], line[1], line[2], str(line[3]), line[4])
        print 'Adding item ' + line[0]
        
        try:
            db.session.add(skills_master)
            db.session.commit()
        except:
            print 'Could not add item ' + line[0]

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
