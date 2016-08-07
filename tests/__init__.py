import os
import unittest
import tempfile

# FIXME: Change this module name
from flask_example.server import app, init_db
from flask_example import models


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['DATABASE'] = "sqlite://"
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            init_db()


__all__ = 'models', 'app'


if __name__ == '__main__':
    unittest.main()
