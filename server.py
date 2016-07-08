# -*- coding: utf-8 -*-

"""
server
~~~~~~

Local web server for the Open Data API.

"""

import os

from app.app import app
from flask_script import Manager

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
