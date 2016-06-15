# -*- coding: utf-8 -*-

"""
app.py
~~~~~~
Management application for the Open Data API.
"""

from app.app import app
from flask_script import Manager
from flask_migrate import MigrateCommand

manager = Manager(app)

# Add the SQLAlchemy database utilities to the manager utility
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
