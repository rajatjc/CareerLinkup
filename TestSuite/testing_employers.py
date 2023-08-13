import unittest
from flask import Flask
from CareerLinkup.models import User, Employer, Job, Applicant
from CareerLinkup import db, bcrypt
from CareerLinkup.forms import User_Login, Employer_Signup, Employer_User_Update, Job_Add, Job_Update, Forgot_Password, Reset_Password, Company_Search
from flask_login import login_user, current_user

# Import the Flask Blueprint 'employer' from the main application file
from CareerLinkup.routes.employers import employer
secret_key = 'secret1234'
# Set up the Flask app for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = secret_key
db.init_app(app)
bcrypt.init_app(app)

# Create test client
client = app.test_client()

class TestEmployerRoutes(unittest.TestCase):
    def setUp(self):
        # Set up the database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the database after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_profile_route(self):
        # Test the '/company/<int:company_id>/profile/' route
        with app.app_context():
            # Add a sample employer to the database for testing
            employer = Employer(name = 'Sample Company', phone = '1234', location = 'abc', tagline='sample', description=
                                'sample', user_id = "temp")
            db.session.add(employer)
            db.session.commit()

            #response = client.get(f'/company/{employer.id}/profile/')
            #self.assertEqual(response.status_code, 200)
            #self.assertIn(b'Sample Company', response.data)

    # Add more test cases for other routes...

if __name__ == '__main__':
    unittest.main()
