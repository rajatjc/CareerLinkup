from flask import render_template, Blueprint, url_for, flash, redirect, request, jsonify
from flask_login import logout_user, current_user
import matplotlib.pyplot as plt
from CareerLinkup import db
from CareerLinkup.models import User, Applicant, Job, jobs_applied, Employer
import io
import base64
import numpy as np


main = Blueprint('main', __name__)

@main.route("/")
def home():
    if current_user.is_authenticated:
        user = current_user.user_role
        return redirect(url_for(f'{user}.{user}_account'))
    return render_template("index.html", title="CareerLinkup | Home")

def insights():
    # Query the database to get the number of applicants for each company
    company_applicants = db.session.query(Employer.name, db.func.count(jobs_applied.c.applicant_id)).\
        join(Job, Employer.id == Job.company_id).\
        join(jobs_applied, Job.id == jobs_applied.c.job_id).\
        group_by(Employer.name).all()

    # Extract company names and the number of applicants from the query results
    companies = [company for company, _ in company_applicants]
    applicants = [int(applicant_count) for _, applicant_count in company_applicants]

    bar_colors = ['#3776AB', '#FF5733', '#7CFC00', '#FFD700', '#9400D3', '#FF8C00', '#FF1493', '#00BFFF']

    # Create a bar chart to visualize the data
    plt.figure(figsize=(10, 6))
    plt.bar(companies, applicants, color=bar_colors, edgecolor='black')  # Use the bar_colors list for the bar colors
    plt.xlabel('Companies', fontsize=12, fontweight='bold')  # Increase font size and add bold to x-axis label
    plt.ylabel('Number of Applicants', fontsize=12, fontweight='bold')  # Increase font size and add bold to y-axis label
    plt.title('Number of Applicants per Company', fontsize=14, fontweight='bold')  # Increase font size and add bold to title
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels, align them right, and reduce font size for better visibility
    plt.yticks(fontsize=10)  # Reduce font size for y-axis labels
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add gridlines to y-axis with dashed style and 70% opacity
    plt.tight_layout()

    # Convert the plot to a base64 encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close('all')  # Explicitly close the plot to avoid exceptions
    plot_base64 = base64.b64encode(buffer.getvalue()).decode()

    return plot_base64

@main.route("/insights")
def show_insights():
    # Call the insights function to generate the plot and get the base64 encoded string
    plot_base64 = insights()

    # Render the template and pass the base64 encoded string
    return render_template("insight_main.html")#, title="CareerLinkup | Insights", plot_base64=plot_base64)

@main.route("/jad")
def show_jad():
    # Call the insights function to generate the plot and get the base64 encoded string
    plot_base64 = insights()

    # Render the template and pass the base64 encoded string
    return render_template("insights.html", title="CareerLinkup | Insights", plot_base64=plot_base64)

@main.route("/about-us")
def about():
    return render_template("about.html", title="CareerLinkup | About Us")

@main.route("/logout")
def logout():
    logout_user()
    flash(f'Logged Out successfully.', 'primary')
    return redirect(url_for('.home'))

@main.route("/filter_employers")
def filter_employers():
    return render_template("filter.html")

# Route to handle the filter parameters and return filtered results
@main.route("/filter_employers", methods=["POST"])
def apply_filter():
    filter_data = request.get_json()

    # Get the individual filter values
    name = filter_data.get("name")
    location = filter_data.get("location")
    tagline = filter_data.get("tagline")

    # Query the Employer table based on the filter parameters
    # If any of the filter fields are provided, include them in the query
    filtered_employers = Employer.query

    if name:
        filtered_employers = filtered_employers.filter_by(name=name)

    if location:
        filtered_employers = filtered_employers.filter_by(location=location)

    if tagline:
        filtered_employers = filtered_employers.filter_by(tagline=tagline)

    # Execute the query to get the filtered results
    filtered_employers = filtered_employers.all()

    # Return the filtered results as JSON
    return jsonify([employer.to_dict() for employer in filtered_employers])

@main.route("/demographic_visualization")
def demographic_visualization():
    # Query the Employer table to get the demographic data
    employers = Employer.query.all()

    # Process the data to calculate the demographics
    demographics = {}
    for employer in employers:
        location = employer.location
        if location in demographics:
            demographics[location] += 1
        else:
            demographics[location] = 1

    # Create the pie chart
    plt.figure(figsize=(8, 8))
    colors = ['red', 'blue', 'green', 'orange', 'purple']  # Add more colors as needed
    plt.pie(demographics.values(), labels=demographics.keys(), autopct="%1.1f%%", colors=colors)
    plt.title("Demographic Visualization of Jobs")

    # Convert the plot to a base64 encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close('all')
    plot_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Render the Flask template with the pie chart
    return render_template("demographic_visualization.html", plot_base64=plot_base64)

@main.route('/salary_growth', methods=['GET', 'POST'])
def salary_growth_comparison():
    if request.method == 'POST':
        current_salary = float(request.form['current_salary'])

        # Retrieve all jobs from the database
        all_jobs = Job.query.all()
        salary_growth_data = []

        for job in all_jobs:
            if job.salary > 0:  # Considering only jobs with a valid salary
                # Fetch the company name from the corresponding Employer record
                company_name = Employer.query.filter_by(id=job.company_id).first().name
                salary_growth = ((job.salary - current_salary) / current_salary) * 100
                salary_growth_data.append((f"{company_name}: {job.title}", salary_growth))

        # Sort jobs based on salary growth for the chart
        salary_growth_data.sort(key=lambda x: x[1], reverse=True)
        job_labels = [item[0] for item in salary_growth_data]
        salary_growth = [item[1] for item in salary_growth_data]

        # Define custom colors for the bars
        colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 'pink', 'cyan', 'brown', 'gray']

        # Generate the chart
        plt.figure(figsize=(10, 6))
        plt.bar(job_labels, salary_growth, color=colors[:len(job_labels)], edgecolor='black')  # Use custom colors for the bars
        plt.xlabel('Company Name - Job Title')
        plt.ylabel('Salary Growth (%)')
        plt.title('Salary Growth Comparison')
        plt.xticks(rotation=45, ha='right')  # Rotate labels and align them to the right
        plt.tight_layout()

        # Convert the chart to a base64 encoded string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        chart_data = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return render_template('chart.html', chart_data=chart_data)

    return render_template('input_page_for_chart.html')