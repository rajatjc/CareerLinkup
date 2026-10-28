from CareerLinkup.models import Applicant, Employer, Job, User


def test_seed_fills_an_empty_database_once(app):
    runner = app.test_cli_runner()

    result = runner.invoke(args=["seed"])
    assert result.exit_code == 0, result.output
    assert Employer.query.count() == 3
    assert Job.query.count() == 5
    assert len(Applicant.query.one().applied_jobs) == 2

    again = runner.invoke(args=["seed"])
    assert again.exit_code != 0
    assert User.query.count() == 5


def test_seeded_accounts_can_log_in(app, client):
    app.test_cli_runner().invoke(args=["seed"])
    response = client.post("/employer/login/", data={"email": "hr@maple.example", "password": "password123"})
    assert response.headers["Location"] == "/employer/account/"
