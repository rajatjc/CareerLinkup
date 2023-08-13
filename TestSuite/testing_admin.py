import unittest
from flask import Flask
from CareerLinkup import db  # Import necessary modules from your application
from CareerLinkup.routes.admin import admin  # Import the 'admin' Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Replace the imports above with actual imports from your application

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"
app.config['SECRET_KEY'] = 'secret1234'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin.admin_login'

app.register_blueprint(admin)

class AdminTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_admin_dashboard(self):
        response = app.get('/admin/dashboard/')
        self.assertIsNotNone(response)

    def test_admin_login(self):
        response = app.get('/admin/login')
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
