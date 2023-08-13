# Import necessary modules and libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from os import path
from sqlalchemy import create_engine
from flask_mail import Mail

# Initialize Flask extensions and other variables
dir = 'CareerLinkupApp'  # The name of the application directory
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing
db = SQLAlchemy()  # Initialize SQLAlchemy for database management
login_manager = LoginManager()  # Initialize LoginManager for user authentication
mail = Mail()  # Initialize Flask-Mail for email support

secret_key = 'secret1234'  # Secret key for session security

# Flask App function with initialized configurations
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = secret_key  # Set the secret key for session security
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///mydata.db"  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Track database modifications
    
    db.init_app(app)  # Initialize the SQLAlchemy database with the Flask app
    bcrypt.init_app(app)  # Initialize Bcrypt with the Flask app
    login_manager.init_app(app)  # Initialize LoginManager with the Flask app
    mail.init_app(app)  # Initialize Flask-Mail with the Flask app

    # Import and register blueprints for different parts of the application
    from .routes.main import main
    from .routes.applicants import applicant
    from .routes.employers import employer
    from .routes.jobs import jobs
    from .routes.errors import errors
    from .routes.admin import admin

    app.register_blueprint(main)  # Main blueprint for the main routes
    app.register_blueprint(applicant)  # Blueprint for applicant routes
    app.register_blueprint(employer)  # Blueprint for employer routes
    app.register_blueprint(jobs)  # Blueprint for job-related routes
    app.register_blueprint(errors)  # Blueprint for error handlers
    app.register_blueprint(admin)  # Blueprint for admin route

    # Custom template filter to format numbers with commas for thousands separator
    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    # Uncomment the following lines during initial database setup to create the tables
    # db.create_all()
    # create_db(app)
    with app.app_context():
        db.create_all()

    return app

# Function to create the SQLite database in the application directory
def create_db(app):
    if not path.exists(f'{dir}/mydata.db'):
        db.create_all(app=app)
