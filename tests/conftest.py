import pytest

from CareerLinkup import bcrypt, create_app, db
from CareerLinkup.models import Admin, Applicant, Employer, Job, User

PASSWORD = "password123"


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test",
        "SERVER_NAME": "localhost",
    })
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def make_user(email, role):
    return User(email=email, user_role=role, password=bcrypt.generate_password_hash(PASSWORD).decode())


@pytest.fixture
def applicant(app):
    applicant = Applicant(f_name="Ada", l_name="Lovelace", phone="5145550100", resume="ada.pdf",
                          user=make_user("ada@example.com", "applicant"))
    db.session.add(applicant)
    db.session.commit()
    return applicant


@pytest.fixture
def employer(app):
    employer = Employer(name="ACME", phone="5145550101", location="Montreal", tagline="We build things",
                        description="Makers of everything", user=make_user("hr@acme.example", "employer"))
    db.session.add(employer)
    db.session.commit()
    return employer


@pytest.fixture
def admin(app):
    admin = Admin(name="Root", phone="5145550102", user=make_user("admin@example.com", "admin"))
    db.session.add(admin)
    db.session.commit()
    return admin


@pytest.fixture
def job(employer):
    job = Job(title="Backend Developer", category="Engineering", type="Full Time",
              description="Build the API", salary=90000, company=employer)
    db.session.add(job)
    db.session.commit()
    return job


def login(client, role, email):
    paths = {"applicant": "/applicant/login", "employer": "/employer/login/", "admin": "/admin/login"}
    return client.post(paths[role], data={"email": email, "password": PASSWORD})
