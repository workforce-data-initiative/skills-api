# -*- coding: utf-8 -*-

"""
etl.py
~~~~~~
OpenSkills API Extract-Transform-Load utility

"""

import csv
import re
import os
import hashlib
import time

from api.v1.models.skills_master import SkillMaster
from api.v1.models.jobs_master import JobMaster
from api.v1.models.jobs_alternate_titles import JobAlternateTitle
from api.v1.models.jobs_unusual_titles import JobUnusualTitle
from api.v1.models.jobs_skills import JobSkill
from api.v1.models.skills_importance import SkillImportance
from api.v1.models.quarters import Quarter
from api.v1.models.geographies import Geography
from api.v1.models.jobs_importance import JobImportance
from api.v1.models.geo_title_count import GeoTitleCount
from api.v1.models.title_count import TitleCount


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
def load_skills_importance():
    """Load the skills importance table"""
    with open(os.path.join('etl', 'etl', 'stage_1', 'ksas_importances.csv'), 'r') as f:
        skills = f.readlines()

        skills = skills[1:]

        found_importance = False
        found_level = False
        level = ''
        importance = ''
        count = 1

        for skill in skills:
            skill_array = skill.split(',')
            onet_soc_code = skill_array[1]
            skill_name = skill_array[3].lower()
            scale = skill_array[4]
            value = skill_array[5]
            
            if not found_importance:
                skill_uuid = SkillMaster.query.filter_by(skill_name = skill_name).first().uuid
                job_uuid = JobMaster.query.filter_by(onet_soc_code = onet_soc_code).first().uuid

                if scale == 'IM':
                    importance = value
                    found_importance = True
            elif not found_level and found_importance:
                if scale == 'LV':
                    level = value
                    found_level = True
                    print 'adding row ' + str(count) + ' of ' + str(len(skills)/2) 
                    skills_importance = SkillImportance(job_uuid, skill_uuid, level, importance)
                    db.session.add(skills_importance)
                    db.session.commit()

                    # reset importance and level
                    found_level = False
                    found_importance = False
                    level = ''
                    importance = ''
                    count += 1

@manager.command
def load_jobs_skills():
    """ Loads the jobs_skills table """

    with open(os.path.join('tmp', 'skills_master_unique_table.tsv'), 'r') as f:
        skills = f.readlines()

    # dump the header
    skills = skills[1:]
    
    for skill in skills:
        skill = skill.strip().split('\t')
        onet_soc_code = str(skill[1])
        skill_name = str(skill[3])
        
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
def load_jobs_importances():
    """ Loads the jobs_importances table """

    # Hardcoding quarter for now
    quarter = Quarter.query.filter_by(year = 2016, quarter = 4).first()
    if not quarter:
        quarter = Quarter(year=2016, quarter=4)
        db.session.add(quarter)
        db.session.commit()

    quarter_id = quarter.quarter_id

    with open(os.path.join('tmp', 'cbsa_jobs.csv'), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                print 'Skipping', row, 'with not enough data'
                continue
            else:
                title, cbsa, importance = row

            if cbsa == '' or title == '':
                print 'Skipping', row, 'with invalid data'
                continue

            kwargs = {
                'geography_name': cbsa,
                'geography_type': 'CBSA'
            }
            geography = Geography.query.filter_by(**kwargs).first()
            if not geography:
                geography = Geography(**kwargs)
                db.session.add(geography)
                db.session.commit()

            job_title_uuid = str(hashlib.md5(title).hexdigest())
            job_importance = JobImportance(
                job_uuid=job_title_uuid,
                quarter_id=quarter_id,
                geography_id=geography.geography_id,
                importance=importance
            )
            db.session.add(job_importance)
        print 'Committing db session'
        db.session.commit()
        print 'Load complete'


def load_geo_quarter_title_counts(filename, year, quarter):
    """ Loads the geo_title_counts table """

    before_time = time.time()
    # Hardcoding quarter for now
    quarter_record = Quarter.query.filter_by(year=year, quarter=quarter).first()
    if not quarter_record:
        quarter_record = Quarter(year=year, quarter=quarter)
        db.session.add(quarter_record)
        db.session.commit()

    quarter_id = quarter_record.quarter_id

    with open(os.path.join('etl/stage_1', filename), 'r') as f:
        reader = csv.reader(f)
        records = []
        for row in reader:
            if len(row) < 3:
                print 'Skipping', row, 'with not enough data'
                continue
            else:
                cbsa, title, count = row

            if cbsa == '' or title == '':
                print 'Skipping', row, 'with invalid data'
                continue

            kwargs = {
                'geography_name': cbsa,
                'geography_type': 'CBSA'
            }
            geography = Geography.query.filter_by(**kwargs).first()
            if not geography:
                geography = Geography(**kwargs)
                db.session.add(geography)
                db.session.commit()

            job_title_uuid = str(hashlib.md5(title).hexdigest())
            records.append(GeoTitleCount(
                job_uuid=job_title_uuid,
                job_title=title,
                quarter_id=quarter_id,
                geography_id=geography.geography_id,
                count=count
            ))
        print 'Saving objects'
        db.session.bulk_save_objects(records)
        db.session.commit()
        after_time = time.time()
        print 'Load complete', str(after_time - before_time), 'seconds'


def load_quarter_title_counts(filename, year, quarter):
    """ Loads the title_counts table """

    # Hardcoding quarter for now
    quarter_record = Quarter.query.filter_by(year=year, quarter=quarter).first()
    if not quarter_record:
        quarter_record = Quarter(year=year, quarter=quarter)
        db.session.add(quarter_record)
        db.session.commit()

    quarter_id = quarter_record.quarter_id

    with open(os.path.join('etl/stage_1', filename), 'r') as f:
        reader = csv.reader(f)
        records = []
        for row in reader:
            if len(row) < 2:
                print 'Skipping', row, 'with not enough data'
                continue
            else:
                title, count = row

            if title == '':
                print 'Skipping', row, 'with invalid data'
                continue

            job_title_uuid = str(hashlib.md5(title).hexdigest())
            records.append(TitleCount(
                job_uuid=job_title_uuid,
                job_title=title,
                quarter_id=quarter_id,
                count=count
            ))
        print 'Saving objects'
        db.session.bulk_save_objects(records)
        db.session.commit()
        print 'Load complete'


@manager.command
def load_all_geo_title_counts():
    for filename in os.listdir('etl/stage_1/'):
        print 'checking', filename
        match = re.match(r"output_geo_title_count_(?P<year>\d{4})Q(?P<quarter>\d).csv", filename)
        if match:
            print 'loading', filename
            year = match.group('year')
            quarter = match.group('quarter')
            load_geo_quarter_title_counts(filename, year, quarter)


@manager.command
def load_all_title_counts():
    for filename in os.listdir('etl/stage_1/'):
        print 'checking', filename
        match = re.match(r"output_title_count_(?P<year>\d{4})Q(?P<quarter>\d).csv", filename)
        if match:
            print 'loading', filename
            year = match.group('year')
            quarter = match.group('quarter')
            load_quarter_title_counts(filename, year, quarter)


@manager.command
def load_all_tables():
    """ Load all tables in sequence """
    load_jobs_master()
    load_skills_master()
    load_jobs_alternate_titles()
    load_jobs_unusual_titles()
    #load_skills_related()
    load_jobs_skills()
    load_jobs_importances()
    load_all_geo_title_counts()
    load_all_title_counts()

if __name__ == '__main__':
    manager.run()
