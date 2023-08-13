import unittest
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from CareerLinkup import db
from CareerLinkup.routes.main import main  # Import the 'main' Blueprint
from flask_sqlalchemy import SQLAlchemy
from unittest.mock import patch

# Replace the imports above with actual imports from your application

# def create_app():
app = Flask(__name__)
app.config['TESTING'] = True
    # db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"
app.config['SECRET_KEY'] = 'secret1234'
db.init_app(app)
bcrypt = Bcrypt(app)

    # Register the blueprint with the appropriate URL prefix
app.register_blueprint(main)

    # login_manager = LoginManager(app)
    # login_manager.login_view = 'admin.admin_login'
#
#     return app
#
# app = create_app()

class MainRoutesTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()
            # self.app = app.test_client()

    def test_home_page(self):
        response = app.get('/')
        self.assertNotEquals(response, 404)
        # Add more assertions based on the expected response data

    @patch('CareerLinkup.routes.main.insights')  # Mock the insights function
    def test_show_insights(self, mock_insights):
        mock_insights.return_value = 'mock_plot_base64'
        response = app.get('/insights')
        self.assertNotEquals(response, 404)
        # self.assertFalse(response)
        # Add more assertions based on the expected response data

    # Add more test cases for other routes and functions

if __name__ == '__main__':
    unittest.main()
