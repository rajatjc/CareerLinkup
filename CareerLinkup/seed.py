import os

import click
from flask import current_app
from flask.cli import with_appcontext
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from CareerLinkup import bcrypt, db
from CareerLinkup.models import Admin, Applicant, Employer, Job, User

DEMO_PASSWORD = "password123"

EMPLOYERS = [
    ("NORTHWIND LABS", "Montreal", "Data tools for small teams", "https://northwind.example", [
        ("Backend Developer", "Engineering", "Full Time", 95000, "Build and run the Python services behind our product."),
        ("Data Analyst Intern", "Data", "Internship", 45000, "Turn customer data into weekly reports."),
    ]),
    ("MAPLE HEALTH", "Toronto", "Software for community clinics", "https://maple.example", [
        ("Frontend Developer", "Engineering", "Full Time", 90000, "Own the patient booking web app."),
        ("QA Analyst", "Quality", "Contract", 70000, "Write and run test plans for each release."),
    ]),
    ("HARBOUR LOGISTICS", "Vancouver", "Shipping, tracked end to end", None, [
        ("DevOps Engineer", "Engineering", "Full Time", 110000, "Keep the tracking platform running on Kubernetes."),
    ]),
]


def demo_resume(name):
    """Write a one-page placeholder resume PDF and return its file name."""
    file_name = "demo-resume.pdf"
    path = os.path.join(current_app.root_path, "static/applicant/resume", file_name)
    pdf = canvas.Canvas(path, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(72, 700, name)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, 676, "Demo resume created by `flask seed`.")
    pdf.save()
    return file_name


def user(email, role):
    return User(email=email, user_role=role, password=bcrypt.generate_password_hash(DEMO_PASSWORD).decode())


@click.command("seed")
@with_appcontext
def seed_command():
    """Fill an empty database with demo accounts, companies and jobs."""
    if User.query.first():
        raise click.ClickException("The database already has users; seed only runs on an empty one.")

    db.session.add(Admin(name="Admin", phone="5145550100", user=user("admin@demo.example", "admin")))

    jobs = []
    for i, (name, location, tagline, website, openings) in enumerate(EMPLOYERS):
        employer = Employer(name=name, phone=f"51455501{i + 1:02d}", location=location, tagline=tagline,
                            description=f"{name.title()} is a demo company created by the seed command.",
                            website=website, user=user(f"hr@{name.split()[0].lower()}.example", "employer"))
        db.session.add(employer)
        for title, category, kind, salary, description in openings:
            jobs.append(Job(title=title, category=category, type=kind, salary=salary,
                            description=description, company=employer))
    db.session.add_all(jobs)

    applicant = Applicant(f_name="Ada", l_name="Lovelace", phone="5145550199",
                          resume=demo_resume("Ada Lovelace"), user=user("ada@demo.example", "applicant"))
    applicant.applied_jobs.extend(jobs[:2])
    db.session.add(applicant)
    db.session.commit()

    click.echo(f"Seeded {len(EMPLOYERS)} employers, {len(jobs)} jobs and 1 applicant.")
    click.echo(f"Log in with any of these (password: {DEMO_PASSWORD}):")
    for account in User.query.order_by(User.user_role, User.email):
        click.echo(f"  {account.user_role:<9} {account.email}")
