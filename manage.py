# -*- coding: utf-8 -*-

"""
app.py
~~~~~~
Management application for the Open Data API.
"""

import os
import hashlib

from app.app import app, db
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)

import uuid

from db.models.skills_master import SkillMaster
from db.models.job_skills import JobSkill
from db.models.jobs import Job
from db.models.jobs import AlternateJobTitle

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
            onet_soc_code = str(line[2])
            onet_element_id = str(line[3])
            skill_name = str(line[4])
            skill_count = int(line[5])
            skill_uuid = str(hashlib.md5(skill_name).hexdigest())

            if (SkillMaster.query.filter_by(skill_name = skill_name).count() == 0):
                skills_master = SkillMaster(skill_uuid, onet_soc_code, \
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

def seed_jobs_master():
    "Populate the jobs database table."
    with open(os.path.join('common', 'occupations.tsv'), 'r') as f:
        occupations = f.readlines()

    occupations = occupations[1:]
    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        if occupation[3] == 'n/a':
            onet_soc_code = occupation[0]
            title = occupation[1].lower()
            description = occupation[2].lower()
            job_uuid = str(hashlib.md5(title).hexdigest())
            job = Job(job_uuid, onet_soc_code, title, description)
           
            print 'Adding Job ' + job.title

            try:
                db.session.add(job)
                db.session.commit()
            except:
                print 'Could not add job ' + job.title

def seed_job_titles():
    with open(os.path.join('common', 'occupations.tsv'), 'r') as f:
        occupations = f.readlines()

    occupations = occupations[1:]
    created_uuids = []
    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        if occupation[1] == 'n/a' and occupation[2] == 'n/a':
            onet_soc_code = occupation[0]
            title = occupation[3].lower()
            job_title_uuid = str(hashlib.md5(title).hexdigest())

            if job_title_uuid not in created_uuids:
                job_uuid = Job.query.filter_by(onet_soc_code = onet_soc_code).first().uuid
            
            
                if job_uuid is not None: 
                    alternate_job_title = AlternateJobTitle(job_title_uuid, title, job_uuid)

                    print 'Adding Job Title ' + alternate_job_title.title

                    try:
                        db.session.add(alternate_job_title)
                        db.session.commit()
                        created_uuids.append(job_title_uuid)
                    except:
                        print 'Could not add job title ' + alternate_job_title.title
                else:
                    print 'Could Not Find Job For Title ' + alternate_job_title.title

@manager.command
def seed_jobs():
    seed_jobs_master()
    seed_job_titles()



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
