# -*- coding: utf-8 -*-

"""
etl.py
~~~~~~
OpenSkills API Extract-Transform-Load utility

"""

import os
import sys
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

    with open(os.path.join('tmp', 'skills_master_table.tsv'), 'r') as f:
        skills = f.readlines()

    # dump the header
    skills = skills[1:]
    total = 0
    duplicate = 0
    added = 0

    added_codes = []

    for skill in skills:
        skill = skill.strip().split('\t')
        #uuid = skill[5]
        skill_name = skill[3]
        uuid = str(hashlib.md5(skill_name).hexdigest())
        onet_element_id = skill[2]
        description = skill[4]
        nlp_a = skill[6]
       
        if uuid not in added_codes:
            skill_master = SkillMaster(uuid, skill_name, onet_element_id, description, nlp_a)

            print 'Adding skill ' + skill_name + ' | ' + uuid
            total += 1
            try:
                added += 1
                db.session.add(skill_master)
                db.session.commit()
                added_codes.append(uuid)
            except:
                added -= 1
                duplicate += 1
                print '\t ---> Duplicate skill ' + skill_name + ' | ' + uuid 
    print '\nSummary'
    print '-------'
    print ' Total skills seen = ' + str(total)
    print ' Total skills added = ' + str(added)
    print ' Total duplicates = ' + str(duplicate)
    print ' Added + Duplicates = ' + str(added + duplicate)

@manager.command
def load_jobs_master():
    """ Loads the jobs_master table """
    with open(os.path.join('tmp', 'job_titles_master_table.tsv'), 'r') as f:
        occupations = f.readlines()

    # dump the header
    occupations = occupations[1:]
    total = 0
    duplicate = 0
    added = 0

    added_codes = []



    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        uuid = occupation[5]
        onet_soc_code = occupation[1]
        title = occupation[2]
        original_title = occupation[3]
        description = str(occupation[4])
        nlp_a = occupation[6]
       
        if title == original_title and uuid not in added_codes:
            job_master = JobMaster(uuid, onet_soc_code, title, original_title, description, nlp_a)

            print 'Adding job ' + title + ' | ' + uuid
            total += 1
            try:
                added += 1
                db.session.add(job_master)
                db.session.commit()
                added_codes.append(uuid)
            except:
                added -= 1
                duplicate += 1
                print 'Duplicate job ' + title + ' | ' + uuid 
    print '\nSummary'
    print '-------'
    print ' Total jobs seen = ' + str(total)
    print ' Total jobs added = ' + str(added)
    print ' Total duplicates = ' + str(duplicate)
    print ' Added + Duplicates = ' + str(added + duplicate)

@manager.command
def load_jobs_alternate_titles():
    """ Loads the jobs_alternate_titles table """

    with open(os.path.join('tmp', 'job_titles_master_table.tsv'), 'r') as f:
        occupations = f.readlines()

    # dump the header
    occupations = occupations[1:]
    total = 0
    duplicate = 0
    added = 0
    added_codes = []

    for occupation in occupations:
        occupation = occupation.strip().split('\t')
        uuid = occupation[5]
        onet_soc_code = occupation[1]
        title = occupation[2]
        original_title = occupation[3]
        description = str(occupation[4])
        nlp_a = occupation[6]
        job_title_uuid = str(hashlib.md5(title).hexdigest())
       
        if title != original_title and job_title_uuid not in added_codes:
            job_alternate_title = JobAlternateTitle(job_title_uuid, title, nlp_a, uuid)

            print 'Adding job ' + title + ' | ' + job_title_uuid
            total += 1
            try:
                added += 1
                db.session.add(job_alternate_title)
                db.session.commit()
                added_codes.append(job_title_uuid)
            except:
                added -= 1
                duplicate += 1
                print 'Duplicate job ' + title + ' | ' + job_title_uuid 
    print '\nSummary'
    print '-------'
    print ' Total jobs seen = ' + str(total)
    print ' Total jobs added = ' + str(added)
    print ' Total duplicates = ' + str(duplicate)
    print ' Added + Duplicates = ' + str(added + duplicate)

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
