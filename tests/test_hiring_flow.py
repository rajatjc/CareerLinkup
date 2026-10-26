from CareerLinkup import db
from CareerLinkup.models import Job, jobs_applied

from conftest import login


def shortlisted(job, applicant):
    row = db.session.query(jobs_applied.c.shortlisted).filter_by(job_id=job.id, applicant_id=applicant.id).one()
    return row.shortlisted


def test_employer_posts_edits_and_removes_a_job(client, employer):
    login(client, "employer", "hr@acme.example")
    job_form = {"title": "Data Engineer", "category": "Data", "type": "Contract",
                "description": "Pipelines and more", "salary": "85000"}

    client.post("/employer/post-jobs/", data=job_form)
    job = Job.query.filter_by(title="Data Engineer").one()
    assert job.company == employer and job.salary == 85000

    client.post(f"/employer/jobs/{job.id}/update", data={**job_form, "title": "Senior Data Engineer"})
    assert db.session.get(Job, job.id).title == "Senior Data Engineer"

    client.post(f"/employer/{job.id}/remove-job/")
    assert db.session.get(Job, job.id) is None


def test_employer_cannot_touch_another_companys_job(client, job):
    client.post("/employer/signup/", data={
        "name": "Globex", "email": "jobs@globex.example", "location": "Toronto", "phone": "4165550100",
        "tagline": "Global excellence", "description": "We make globes", "password": "password123",
    })
    assert client.get(f"/employer/jobs/{job.id}/update").status_code == 403
    assert client.post(f"/employer/{job.id}/remove-job/").status_code == 403
    assert client.get(f"/employer/applicants/{job.id}").status_code == 403


def test_apply_shortlist_and_withdraw(app, client, applicant, job):
    login(client, "applicant", "ada@example.com")
    assert client.get(f"/applicant/application/{job.id}").status_code == 405  # applying changes data, so POST only

    client.post(f"/applicant/application/{job.id}")
    assert job in applicant.applied_jobs

    again = client.post(f"/applicant/application/{job.id}", follow_redirects=True)
    assert b"already applied" in again.data
    assert len(applicant.applied_jobs) == 1

    client.get("/logout")
    login(client, "employer", "hr@acme.example")
    assert b"Ada" in client.get(f"/employer/applicants/{job.id}").data
    client.post(f"/employer/shortlist/{job.id}/{applicant.id}")
    assert shortlisted(job, applicant)
    assert client.post(f"/employer/shortlist/{job.id}/999").status_code == 404

    client.post(f"/employer/list-applicant/{job.id}/{applicant.id}")
    assert not shortlisted(job, applicant)

    client.get("/logout")
    login(client, "applicant", "ada@example.com")
    client.post(f"/applicant/{job.id}/remove-job/")
    assert job not in applicant.applied_jobs
    assert client.post(f"/applicant/{job.id}/remove-job/").status_code == 404


def test_admin_dashboard_counts(client, admin, applicant, job):
    login(client, "admin", "admin@example.com")
    response = client.get("/admin/dashboard/")
    assert response.status_code == 200
    for path in ["/admin/jobs-list/", "/admin/employers/", "/admin/applicants/", "/admin/reports/", "/admin/settings/"]:
        assert client.get(path).status_code == 200, path


def test_first_admin_can_only_be_created_once(client, admin):
    response = client.get("/admin/create")
    assert response.headers["Location"] == "/admin/login"
