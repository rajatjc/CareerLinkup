from unittest import mock

from CareerLinkup import bcrypt, db
from CareerLinkup.models import User

from conftest import PASSWORD, login


def test_applicant_login_and_logout(client, applicant):
    response = login(client, "applicant", "ada@example.com")
    assert response.headers["Location"] == "/applicant/account"
    assert client.get("/applicant/account").status_code == 200

    client.get("/logout")
    assert client.get("/applicant/account").status_code == 302


def test_wrong_password_is_rejected(client, applicant):
    response = client.post("/applicant/login", data={"email": "ada@example.com", "password": "nope-nope"})
    assert response.status_code == 200
    assert b"Invalid Email or Password" in response.data


def test_accounts_cannot_log_in_through_another_roles_page(client, employer):
    response = client.post("/applicant/login", data={"email": "hr@acme.example", "password": PASSWORD})
    assert b"Invalid Email or Password" in response.data


def test_role_pages_require_the_right_role(client, applicant):
    login(client, "applicant", "ada@example.com")
    response = client.get("/employer/account/")
    assert response.status_code == 302
    assert response.headers["Location"].startswith("/employer/login/")


def test_login_follows_local_next(client, applicant):
    response = client.post("/applicant/login?next=/jobs/", data={"email": "ada@example.com", "password": PASSWORD})
    assert response.headers["Location"] == "/jobs/"


def test_login_ignores_offsite_next(client, applicant):
    for target in ["https://evil.example", "//evil.example", "/\\evil.example"]:
        client.get("/logout")
        response = client.post(f"/applicant/login?next={target}", data={"email": "ada@example.com", "password": PASSWORD})
        assert response.headers["Location"] == "/applicant/account"


def test_employer_signup_creates_account(client):
    response = client.post("/employer/signup/", data={
        "name": "Globex", "email": "jobs@globex.example", "location": "toronto", "phone": "4165550100",
        "tagline": "Global excellence", "description": "We make globes", "password": PASSWORD,
    })
    assert response.headers["Location"] == "/employer/account/"
    user = User.query.filter_by(email="jobs@globex.example").one()
    assert user.employers.name == "GLOBEX"
    assert user.employers.location == "Toronto"


def test_signup_rejects_taken_email(client, employer):
    response = client.post("/employer/signup/", data={
        "name": "Globex", "email": "hr@acme.example", "location": "Toronto", "phone": "4165550100",
        "tagline": "Global excellence", "description": "We make globes", "password": PASSWORD,
    })
    assert b"This email is Taken" in response.data


class TestPasswordReset:
    def test_known_email_gets_a_link(self, client, applicant):
        with mock.patch("CareerLinkup.utils.mail.send") as send:
            client.post("/applicant/password-reset", data={"email": "ADA@example.com"})
        assert send.call_count == 1
        assert "/applicant/password-reset/" in send.call_args.args[0].html

    def test_unknown_email_and_wrong_role_send_nothing_and_look_the_same(self, client, applicant):
        with mock.patch("CareerLinkup.utils.mail.send") as send:
            unknown = client.post("/applicant/password-reset", data={"email": "who@example.com"}, follow_redirects=True)
            wrong_role = client.post("/employer/password-reset", data={"email": "ada@example.com"}, follow_redirects=True)
        assert send.call_count == 0
        assert b"If that email belongs to an account" in unknown.data
        assert b"If that email belongs to an account" in wrong_role.data

    def test_mail_failure_does_not_crash(self, client, applicant):
        with mock.patch("CareerLinkup.utils.mail.send", side_effect=ConnectionRefusedError):
            response = client.post("/applicant/password-reset", data={"email": "ada@example.com"})
        assert response.status_code == 302

    def test_token_resets_password_once(self, client, applicant):
        token = applicant.user.get_reset_token()
        new = {"password": "brand-new-pass", "confirm_password": "brand-new-pass"}

        assert client.post(f"/applicant/password-reset/{token}", data=new).headers["Location"] == "/applicant/login"
        assert bcrypt.check_password_hash(db.session.get(User, applicant.user.id).password, "brand-new-pass")
        assert User.verify_reset_token(token) is None

    def test_bad_and_expired_tokens_are_rejected(self, app, applicant):
        assert User.verify_reset_token("not-a-token") is None
        token = applicant.user.get_reset_token()
        app.config["RESET_TOKEN_MAX_AGE"] = -1
        assert User.verify_reset_token(token) is None
