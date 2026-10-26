from conftest import login


def test_salary_growth_chart(client, job):
    response = client.post("/salary_growth", data={"current_salary": "60000"})
    assert response.status_code == 200
    assert b"data:image/png;base64," in response.data


def test_salary_growth_rejects_zero_and_garbage(client, job):
    for value in ["0", "-5", "abc", ""]:
        assert client.post("/salary_growth", data={"current_salary": value}).status_code == 400


def test_applicants_per_company_chart(client, applicant, job):
    login(client, "applicant", "ada@example.com")
    client.post(f"/applicant/application/{job.id}")
    assert b"data:image/png;base64," in client.get("/jad").data


def test_demographics_chart(client, employer):
    assert b"data:image/png;base64," in client.get("/demographic_visualization").data


def test_demographics_with_no_employers_redirects(client):
    response = client.get("/demographic_visualization", follow_redirects=True)
    assert response.status_code == 200
    assert b"nothing to chart" in response.data


def test_resume_builder_returns_a_pdf_even_with_markup_characters(client):
    response = client.post("/applicant/create-resume", data={
        "name": "Ada <Lovelace>", "email": "ada@example.com", "phone": "555",
        "summary": "Math & engines", "education": "Self-taught\nTutored by De Morgan", "experience": "Note G <b",
    })
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")
