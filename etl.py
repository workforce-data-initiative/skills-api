# -*- coding: utf-8 -*-

"""
etl.py
~~~~~~
OpenSkills API Extract-Transform-Load utility

"""

import os
import hashlib
import uuid

from api.v1_0.models.skills_master import SkillMaster
from api.v1_0.models.jobs_master import JobMaster
from api.v1_0.models.jobs_alternate_titles import JobAlternateTitle
from api.v1_0.models.jobs_unusual_titles import JobUnusualTitle
from api.v1_0.models.jobs_skills import JobSkill

from app.app import app, db
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app, with_default_commands=False)

# Add the SQLAlchemy migration utility
manager.add_command('db', MigrateCommand)

@manager.command
def load_skills_master():
    """ Loads the skills_master table """

    with open(os.path.join('tmp', 'skills_master.tsv'), 'r') as f:
        skills = f.readlines()

    # dump the header
    skills = skills[1:]
    
    # collect unique skills from list of skills
    visited_skills = []
    count = 0

    for skill in skills:
        skill = skill.strip().split('\t')
        if str(skill[2]) not in visited_skills:
            onet_soc_code = str(skill[0])
            onet_element_id = str(skill[1])
            skill_name = str(skill[2])
            skill_count = int(skill[3])
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
                    print '\t ----> Could not add skill ' + skill_name
            else:
                print 'Skipping ' + skill_name
                visited_skills.append(skill_name)


@manager.command
def load_jobs_master():
    """ Loads the jobs_master table """
    with open(os.path.join('tmp', 'jobs_master.tsv'), 'r') as f:
        occupations = f.readlines()

    # dump the header
    occupations = occupations[1:]
    
    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        if occupation[3] == 'n/a':
            onet_soc_code = str(occupation[0])
            title = occupation[1]
            description = occupation[2]
            job_uuid = str(hashlib.md5(title).hexdigest())
            job_master = JobMaster(job_uuid, onet_soc_code, title, description)

            print 'Adding job ' + title

            try:
                db.session.add(job_master)
                db.session.commit()
            except:
                print '\t ----> Could not add job ' + title

@manager.command
def load_jobs_alternate_titles():
    """ Loads the jobs_alternate_titles table """

    with open(os.path.join('tmp', 'jobs_master.tsv'), 'r') as f:
        occupations = f.readlines()

    # dump the header
    occupations = occupations[1:]
    created_uuids = []
    
    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        if occupation[1] == 'n/a' and occupation[2] == 'n/a':
            onet_soc_code = str(occupation[0])
            title = occupation[3]
            job_title_uuid = str(hashlib.md5(title).hexdigest())
            
            if job_title_uuid not in created_uuids:
                job_uuid = JobMaster.query.filter_by(onet_soc_code = onet_soc_code).first().uuid
                if job_uuid is not None:
                    alternate_job_title = JobAlternateTitle(job_title_uuid, title, job_uuid)

                    print 'Adding job title ' + title

                try:
                    db.session.add(alternate_job_title)
                    db.session.commit()
                    created_uuids.append(job_title_uuid)
                except:
                    print '\t ----> Could not add job title' + title
            else:
                print 'Could not find job for title ' + title
@manager.command
def load_skills_related():
    """ Loads the skills_related table """
    pass

@manager.command
def load_jobs_skills():
    """ Loads the jobs_skills table """

    with open(os.path.join('tmp', 'skills_master.tsv'), 'r') as f:
        skills = f.readlines()

    # dump the header
    skills = skills[1:]
    
    for skill in skills:
        skill = skill.strip().split('\t')
        onet_soc_code = str(skill[0])
        onet_element_id = str(skill[1])
        skill_name = str(skill[2])
        skill_count = int(skill[3])
        
        skill_uuid = SkillMaster.query.filter_by(skill_name = skill_name).first().uuid
        job_uuid = JobMaster.query.filter_by(onet_soc_code = onet_soc_code).first().uuid

        if skill_uuid is not None and job_uuid is not None:
            jobs_skills = JobSkill(job_uuid, skill_uuid)
        
            if JobSkill.query.filter_by(job_uuid = job_uuid).filter_by(skill_uuid = skill_uuid).count() == 0:
                try:
                    print 'Loading skill ' + skill_uuid + ' with onet-soc-code ' + onet_soc_code
                    db.session.add(jobs_skills)
                    db.session.commit()
                except:
                    print '\t ----> Could not add skill ' + skill_name
            else:
                print 'Skipping ' + skill_name + ' ' + job_uuid
        else:
            print 'Cannot match jobs to skill ' + skill_name

@manager.command
def load_jobs_unusual_titles():
    """ Loads the jobs_unusual_titles table """
    with open(os.path.join('tmp', 'interesting_job_titles.csv'), 'r') as f:
        occupations = f.readlines()

    # dump the header
    #occupations = occupations[1:]
    
    created_uuids = []
    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        title = str(occupation[0])
        description = str(occupation[1])
        onet_soc_code = str(occupation[2])
        job_title_uuid = str(hashlib.md5(title).hexdigest())
        
        if job_title_uuid not in created_uuids:
            job_uuid = JobMaster.query.filter_by(onet_soc_code = onet_soc_code).first().uuid
            if job_uuid is not None:
                unusual_job_title = JobUnusualTitle(job_title_uuid, title, description, job_uuid)

                print 'Adding unusual job title ' + title

                try:
                    db.session.add(unusual_job_title)
                    db.session.commit()
                except:
                    print '\t ----> Could not add unusual job title' + title
            else:
                print 'Could not find job for unusual title ' + title

@manager.command
def load_all_tables():
    """ Load all tables in sequence """
    load_jobs_master()
    load_skills_master()
    load_jobs_alternate_titles()
    load_jobs_unusual_titles()
    #load_skills_related()
    load_jobs_skills()

if __name__ == '__main__':
    manager.run()
