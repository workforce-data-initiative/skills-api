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

# Add the SQLAlchemy database utilities to the manager utility
manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    "Populate the database tables."
    with open(os.path.join('common', 'skills_master.csv'), 'r') as f:
        lines = f.readlines()

    # dump the header
    lines = lines[1:]
    
    for line in lines:
        line = line.strip().split(',')[1:]
        skills_master = SkillsMaster(line[0], line[1], line[2], str(line[3]), line[4])
        print 'Adding item ' + line[0]
        
        db.session.add(skills_master)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
