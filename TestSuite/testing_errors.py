import unittest
from flask import Flask
from CareerLinkup.routes.errors import errors  # Import the 'errors' Blueprint
from flask_sqlalchemy import SQLAlchemy
from CareerLinkup import db
from flask_bcrypt import Bcrypt

# Replace the imports above with actual imports from your application
app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"
app.config['SECRET_KEY'] = 'secret1234'
db.init_app(app)
bcrypt = Bcrypt(app)
app.register_blueprint(errors)

class ErrorsRoutesTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()
        # self.app = app.test_client()

    def test_error_403(self):
        response = app.get('/errors/403')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_error_404(self):
        response = app.get('/errors/404')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_error_405(self):
        response = app.get('/errors/405')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_error_500(self):
        response = app.get('/errors/500')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

if __name__ == '__main__':
    unittest.main()
