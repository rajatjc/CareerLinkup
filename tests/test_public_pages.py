import pytest


@pytest.mark.parametrize("path", [
    "/",
    "/about-us",
    "/jobs/",
    "/jobs/categories/",
    "/companies/",
    "/applicant/login",
    "/applicant/signup",
    "/employer/login/",
    "/employer/signup/",
    "/admin/login",
    "/applicant/password-reset",
    "/employer/password-reset",
    "/admin/password-reset",
    "/applicant/create-resume",
    "/salary_growth",
    "/filter_employers",
])
def test_page_renders(client, path):
    assert client.get(path).status_code == 200


def test_unknown_page_uses_custom_404(client):
    response = client.get("/no-such-page")
    assert response.status_code == 404
    assert b"404" in response.data


def test_job_list_and_details_show_the_job(client, job):
    assert b"Backend Developer" in client.get("/jobs/").data
    assert b"Build the API" in client.get(f"/jobs/{job.id}/details/").data


def test_missing_job_is_404(client):
    assert client.get("/jobs/999/details/").status_code == 404


def test_job_search_matches_title_and_location(client, job):
    found = client.post("/jobs/search", data={"title": "Backend", "location": "Mont"})
    missing = client.post("/jobs/search", data={"title": "Backend", "location": "Toronto"})
    assert b"Backend Developer" in found.data
    assert b"Backend Developer" not in missing.data


def test_job_search_tolerates_missing_fields(client, job):
    assert client.post("/jobs/search", data={}).status_code == 200


def test_company_profile(client, employer):
    assert b"ACME" in client.get(f"/company/{employer.id}/profile/").data


def test_filter_employers_returns_json(client, employer):
    response = client.post("/filter_employers", json={"location": "Montreal"})
    assert [e["name"] for e in response.get_json()] == ["ACME"]
    assert client.post("/filter_employers", json={"location": "Paris"}).get_json() == []
