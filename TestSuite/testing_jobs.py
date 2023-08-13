import unittest
from flask import Flask
from CareerLinkup import db

from flask_bcrypt import Bcrypt
from CareerLinkup.routes.jobs import jobs  # Import the 'jobs' Blueprint
from flask_sqlalchemy import SQLAlchemy

# Replace the imports above with actual imports from your application

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"
app.config['SECRET_KEY'] = 'secret1234'
db.init_app(app)
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)
#login_manager.login_view = 'admin.admin_login'

app.register_blueprint(jobs)
# client
class JobsRoutesTestCase(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()
        # global client
        # client = app.test_client()

    def test_job_list(self):
        response = app.get('/jobs/list/')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_job_profile(self):
        # Assuming you have a valid job_id
        job_id = 1
        response = app.get(f'/jobs/{job_id}/details/')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_job_categories(self):
        response = app.get('/jobs/categories/')
        self.assertNotEquals(response, 404)
        # Add more assertions based on the expected response data

    def test_job_filtered(self):
        # Assuming you have a valid category
        category = 'example_category'
        response = app.get(f'/jobs/categories/{category}')
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

    def test_job_search(self):
        # Assuming you have valid form data
        form_data = {
            'title': 'example_title',
            'location': 'example_location'
        }
        response = app.post('/jobs/search', data=form_data)
        self.assertIsNotNone(response)
        # Add more assertions based on the expected response data

if __name__ == '__main__':
    unittest.main()
