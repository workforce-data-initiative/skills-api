from app import app
import unittest
from flask_migrate import upgrade


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config.from_object('config.test_config.Config')
        self.app = app.app.test_client()
        self.app.testing = True
        with app.app.app_context():
            upgrade()
        app.db.session.begin(subtransactions=True)

    def tearDown(self):
        app.db.session.rollback()
        app.db.session.close()
