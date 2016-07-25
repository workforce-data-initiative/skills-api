import sys
sys.path.append('/var/www/skills-api')
activate_this = '/var/www/skills-api/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from app.app import app as application
