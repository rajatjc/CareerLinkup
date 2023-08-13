
import io

from flask import Blueprint, url_for, flash, redirect, abort, request, render_template, make_response
from flask_login import login_user, current_user
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from CareerLinkup import db, bcrypt
from CareerLinkup.forms import User_Login, Applicant_Signup, Applicant_User_Update, Forgot_Password, Reset_Password
from CareerLinkup.models import User, Applicant, Job, jobs_applied as applied
from CareerLinkup.utils import save_file, remove_file, user_role_required, send_pwd_reset_email



applicant = Blueprint('applicant', __name__)

# Applicant Dashboard
@applicant.route("/applicant/account")
@user_role_required('applicant')
def applicant_account():
    user = current_user.applicants
    jobs = user.applied_jobs
    query = db.session.query(applied).join(Applicant).filter(Applicant.id==user.id).all() 
    shortlists = [ i for i in query if i.shortlisted]

    return render_template("applicants/account.html", title="Applicant | Account", user=user, jobs=jobs, shortlists=shortlists)


@applicant.route("/applicant/application/<int:job_id>")
@user_role_required('applicant')
def apply_for_job(job_id):
    user = current_user.applicants
    job = Job.query.get_or_404(job_id)
    
    user.applied_jobs.append(job)
    db.session.commit()

    flash(f'Application sent Successfully!', 'success')
    return redirect(url_for('.jobs_applied'))

@applicant.route("/applicant/jobs-applied")
@user_role_required('applicant')
def jobs_applied():
    user = current_user.applicants
    page = request.args.get('page', 1, type=int)
    jobs = db.session.query(Job, applied.c.date_applied, applied.c.shortlisted).select_from(Job).join(applied).join(Applicant).filter(Applicant.id==user.id).order_by(applied.c.date_applied.desc()).paginate(page=page, per_page=15)

    return render_template("applicants/jobs.html", title="CareerLinkup | Applied Jobs", jobs=jobs)
@applicant.route("/applicant/shortlisted-jobs")
@user_role_required('applicant')
def shortlisted_jobs():
    user = current_user.applicants
    jobs = db.session.query(Job).join(applied).join(Applicant).filter((Applicant.id==user.id) & (applied.c.shortlisted)).all() 

    return render_template("applicants/shortlists.html", title="CareerLinkup | Applied Jobs", jobs=jobs)

@applicant.route("/applicant/<int:job_id>/remove-job/", methods=['POST'])
@user_role_required('applicant')
def remove_job(job_id):
    user = current_user.applicants
    job = Job.query.get_or_404(job_id)
    user.applied_jobs.remove(job)

    db.session.commit()
            
    flash(f'Job removed from the list successfully', 'success')
    return redirect(url_for('.jobs_applied'))

@applicant.route("/applicant/<int:applicant_id>/delete-image", methods=['POST'])
@user_role_required('applicant')
def delete_image(applicant_id):
    user = Applicant.query.get_or_404(applicant_id)
    if not user.user == current_user:
        abort(403)

    if user.image and user.image != "anony.png":
        file = f'applicant/image/{str(user.image)}'
        try:
            remove_file(file)
            user.image = 'anony.png'
            db.session.commit()
            flash(f'Image Removed Successfully!', category='success')
        except FileNotFoundError:
            user.image = 'anony.png'
            db.session.commit()
            flash(f'File not Found!', category='danger')
    
    return redirect(url_for('.settings'))


# Signing in Applicant user
@applicant.route("/applicant/login", methods=['GET', 'POST'])
def applicant_login():
    if current_user.is_authenticated and current_user.applicants:
        return redirect(url_for('.applicant_account'))
    form = User_Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.applicants and bcrypt.check_password_hash(user.password, form.password.data):
            match = Applicant.query.filter_by(user_id=user.id).first()
            login_user(user)
            flash(f'Logged in as {match.l_name}!', 'success')
            return redirect(request.args.get('next') or url_for('.applicant_account'))
        else:
            flash(f'Invalid Email or Password! Please Try Again.', 'danger')
    return render_template("applicants/login.html", title="CareerLinkup | Applicant Login", form=form)


# Applicant User password reset request
@applicant.route("/applicant/password-reset", methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated and current_user.applicants:
        return redirect(url_for('.applicant_account'))
    form = Forgot_Password()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                send_pwd_reset_email(user, 'applicant', user.applicants.f_name)
                flash('A password reset link has been sent to your email', 'info')
                return redirect(url_for('.applicant_login'))
            except:
                flash('Something went wrong! Please Try Again.', 'warning')
                return redirect(url_for('.password_reset_request'))
        else:
            flash('Email not registered. Send the email you registered your account with.', 'warning')
            return redirect(url_for('.password_reset_request'))
    return render_template("forgot_password.html", title="Applicant | Reset Password", form=form)

# Applicant user password reset token
@applicant.route("/applicant/password-reset/<string:token>", methods=['GET', 'POST'])
def password_reset_link(token):
    if current_user.is_authenticated and current_user.applicants:
        return redirect(url_for('.applicant_account'))
    user = User.verify_reset_token(token)
    if not user:
        flash('The link is either invalid or has expired!', 'warning')
        return redirect(url_for('.password_reset_request'))
          
    form = Reset_Password()
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = pw_hash
        db.session.commit()

        flash('Your Password has been updated', 'success')
        return redirect(url_for('.applicant_login'))
    
    return render_template("reset_password.html", title="Applicant | Reset Password", form=form)


# Applicant Account Settings
@applicant.route("/applicant/settings", methods=['GET','POST'])
@user_role_required('applicant')
def settings():
    user = current_user.applicants
    form = Applicant_User_Update()

    if form.validate_on_submit():
        user.f_name = form.f_name.data.strip().capitalize()
        user.l_name = form.l_name.data.strip().capitalize()
        user.user.email = form.email.data.lower()
        user.phone = form.phone.data 

        if form.resume.data:
            new_file = save_file('applicant/resume/', form.resume.data)
            if new_file:
                old_file = f'applicant/resume/{str(user.resume)}'
                try:
                    remove_file(old_file)
                except FileNotFoundError:
                    flash(f'File or Directory not found!', 'danger')
                user.resume = new_file

        if form.image.data:
            img = save_file('applicant/image/', form.image.data)
            if img:
                if user.image != 'anony.png':
                    file = f'applicant/image/{str(user.image)}'
                    remove_file(file)
                user.image = img

        db.session.commit()
        flash(f'Account Updated Successfully.', 'success')
        return redirect(url_for('.settings'))

    form.f_name.data = user.f_name 
    form.l_name.data = user.l_name
    form.email.data = user.user.email
    form.phone.data = user.phone

    return render_template("applicants/settings.html", title="CareerLinkup | Applicant Settings", form=form, user = user)





# Applicant user registration
@applicant.route("/applicant/signup", methods=['POST', 'GET'])
def applicant_signup():
    if current_user.is_authenticated and current_user.applicants:
        return redirect(url_for('.applicant_account'))
    form = Applicant_Signup()
    if form.validate_on_submit():
        resume = save_file('applicant/resume/', form.resume.data)
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(email=form.email.data.lower(), user_role='applicant', password=pw_hash)
        db.session.add(user)

        if form.image.data:
            image = save_file('applicant/image/', form.image.data) 
            applicant = Applicant(f_name=form.f_name.data.strip().capitalize(), l_name=form.l_name.data.strip().capitalize(), phone=form.phone.data, resume=resume, image=image, user=user)
            db.session.add(applicant)
            db.session.commit()
        else:
            applicant = Applicant(f_name=form.f_name.data.strip().capitalize(), l_name=form.l_name.data.strip().capitalize(), phone=form.phone.data, resume=resume, user=user)
            db.session.add(applicant)
            db.session.commit()

        flash(f'Account Successfully created for {form.email.data}!', 'success')
        login_user(user, remember=True)
        return redirect(url_for('.settings'))
    return render_template("applicants/signup.html", title="CareerLinkup | Applicant Signup", form=form)

# Route to create a resume
@applicant.route("/applicant/create-resume", methods=["GET", "POST"])
def create_resume():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        summary = request.form.get("summary")
        education = request.form.get("education")
        experience = request.form.get("experience")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Customize styles for a more beautiful resume
        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=24, textColor='black')
        heading_style = ParagraphStyle('Heading2', parent=styles['Heading2'], fontSize=14, textColor='black')
        normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=12, textColor='black')

        content = []

        # Add name in a larger, more prominent title style
        content.append(Paragraph(name, title_style))
        content.append(Spacer(1, 12))

        content.append(Paragraph("Contact Information", heading_style))
        content.append(Paragraph(f"Email: {email}", normal_style))
        content.append(Paragraph(f"Phone: {phone}", normal_style))
        content.append(Spacer(1, 12))

        content.append(Paragraph("Summary", heading_style))
        content.append(Paragraph(summary, normal_style))
        content.append(Spacer(1, 12))

        content.append(Paragraph("Education", heading_style))
        education_lines = education.split('\n')
        for line in education_lines:
            content.append(Paragraph(line, normal_style))
            content.append(Spacer(1, 6))  # Adjust the spacing as needed

        content.append(Paragraph("Experience", heading_style))
        experience_lines = experience.split('\n')
        for line in experience_lines:
            content.append(Paragraph(line, normal_style))
            content.append(Spacer(1, 6))  # Adjust the spacing as needed

        doc.build(content)
        buffer.seek(0)

        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
        return response

    return render_template("create-resume.html")
