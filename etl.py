# -*- coding: utf-8 -*-

"""
etl.py
~~~~~~
OpenSkills API Extract-Transform-Load utility

"""

import os
import hashlib
import uuid

from app.app import app, db
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app, with_default_commands=False)

# Add the SQLAlchemy migration utility
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
