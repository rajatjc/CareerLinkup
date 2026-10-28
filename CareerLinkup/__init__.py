# Import necessary modules and libraries
import matplotlib

matplotlib.use("Agg")  # Charts are rendered to PNG on the server; there is no display to draw on.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from CareerLinkup.config import Config

# Initialize Flask extensions
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing
db = SQLAlchemy()  # Initialize SQLAlchemy for database management
login_manager = LoginManager()  # Initialize LoginManager for user authentication
mail = Mail()  # Initialize Flask-Mail for email support
csrf = CSRFProtect()  # Require a CSRF token on every POST, not just the WTForms ones


# Flask App function with initialized configurations.
# Pass a dict of overrides (for example in tests) to replace any setting from Config.
def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if overrides:
        app.config.update(overrides)

    db.init_app(app)  # Initialize the SQLAlchemy database with the Flask app
    bcrypt.init_app(app)  # Initialize Bcrypt with the Flask app
    login_manager.init_app(app)  # Initialize LoginManager with the Flask app
    mail.init_app(app)  # Initialize Flask-Mail with the Flask app
    csrf.init_app(app)  # Initialize CSRF protection with the Flask app

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

    # `flask --app main seed` fills an empty database with demo data
    from .seed import seed_command
    app.cli.add_command(seed_command)

    # Custom template filter to format numbers with commas for thousands separator
    @app.template_filter()
    def numberFormat(value):
        return format(int(value), ',d')

    with app.app_context():
        db.create_all()

    return app
