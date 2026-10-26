import re

from conftest import PASSWORD


def token_from(html):
    return re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html).group(1)


def test_posts_without_a_token_are_rejected(client, app, applicant, job):
    app.config["WTF_CSRF_ENABLED"] = True
    page = client.get("/applicant/login").get_data(as_text=True)
    client.post("/applicant/login", data={"email": "ada@example.com", "password": PASSWORD, "csrf_token": token_from(page)})

    assert client.post(f"/applicant/application/{job.id}").status_code == 400

    token = token_from(client.get(f"/jobs/{job.id}/details/").get_data(as_text=True))
    assert client.post(f"/applicant/application/{job.id}", data={"csrf_token": token}).status_code == 302


def test_filter_endpoint_accepts_token_header(client, app, employer):
    app.config["WTF_CSRF_ENABLED"] = True
    assert client.post("/filter_employers", json={}).status_code == 400

    page = client.get("/filter_employers").get_data(as_text=True)
    token = re.search(r'"X-CSRFToken": "([^"]+)"', page).group(1)
    assert client.post("/filter_employers", json={}, headers={"X-CSRFToken": token}).status_code == 200
