# CareerLinkup

## Description
CareerLinkup is a web application that serves as a comprehensive career services platform, connecting job seekers with employers. The platform facilitates the job search process by allowing job seekers to create and update their portfolios and enabling employers to post job offers. With CareerLinkup, users can easily find and apply for relevant job opportunities, while employers can efficiently search and shortlist candidates. The platform aims to streamline the hiring process, benefitting both job seekers and employers.

## Team Name: JAN-Soen6011summer2023

### Team Members (Name, Github Username, Role)

- Arpit Sehgal: [arpit1102](https://github.com/arpit1102) : Team Lead and Backend Devleoper
- Rajat Sharma: [rajatjc](https://github.com/rajatjc) :  Backend Developer + Documentation
- Jatish Bhatia: [jatishbhatia](https://github.com/jatishbhatia) : Database Developer + Minutes of Meeting
- Vikram Singh Brahm: [vikramsinghbrahm](https://github.com/vikramsinghbrahm) : Documentation + Integration Tester
- Harika Maddukuri: [harika89](https://github.com/harika89) : UI/UX Developer
- Nandini Bibra: [nandinibibra-96](https://github.com/nandinibibra-96) : Database Developer

### Roles and Responsibilities

- Arpit Sehgal:
  - Serve as the Team Lead and monitor development.
  - Backend development using Python.
  - Code Review.
  - Documentation

- Rajat:

  - Write Python programs to facilitate backend logic.
  - Conduct regular code reviews.
  - Host the web service.
  - Documentation.

- Jatish Bhatia:
  - Write Python programs to facilitate backend logic.
  - Conduct regular code reviews.
  - Host the web service.
  - Documentation.

- Vikram Singh Brahm:
  - Perform integration/beta testing.
  - Documentation.
  - Generate automation scripts if required.
  - UI development

- Harika:
  - Create UI/UX design for the application.
  - Document the code.
  - Conduct code reviews.

- Nandini Bibra:
  - Design database architecture
  - Work on developing the database and managing data.
  - Document all the tabular and code data.
  - Conduct code reviews.


## Flask Application Setup and Running

### Prerequisites

- Python 3.10.7
- virtualenv

### Installation

1. Check Python version:

   ```python3 --version```

   Output:

   ```Python 3.10.7```

2. Install virtualenv:

   ```pip install virtualenv```

3. Create a virtual environment:

   ```virtualenv venv```

4. Activate the virtual environment (on macOS/Linux):

   ```source venv/bin/activate```

   or (on Windows):
   
   ```venv\Scripts\activate```

5. Install the required dependencies for the Flask application from `requirements.txt`:

   ```pip install -r requirements.txt```

### Running

1. After setting up the virtual environment and installing the requirements, you can run the main Python file of the Flask application:

   ```python3 main.py```

2. The Flask application will be running locally on your machine at `http://localhost:5002/`. Open this URL in your web browser to access the application.

### Deactivating the Virtual Environment

After you're done using the Flask application, you can deactivate the virtual environment by running:

```deactivate```


### Project Approach and Technology
The project follows an Agile development approach, allowing for iterative and incremental development. HTML, CSS and Javascript are used for developing the user interface while python is used as the programming language for developing backend logic. Flask, a python module is used to launch the application as a web service so make the program platform independent and provide the end user with a browser based application experience.SQLAlchemy will be used to maintain database for all services and core features.

### Reasoning behind technologies
- Flask:
  - The primary purpose to choose Flask is its ease of use.
  - Flask is a lightweight and easy-to-use web framework for Python, making it ideal for small to medium-sized projects like our Employee Portal.
  - It provides essential tools and features needed for building web applications while allowing for flexibility and scalability.

- Python:
  - Python is known to majority of team members.
  - Python is a versatile and widely-used programming language, known for its simplicity and readability.
  - Using Python allows for rapid development, reducing the time needed to implement features and maintain the application.

- SQLite:
  - SQLite is free for use for the project.
  - SQLite is a self-contained, serverless, and zero-configuration database engine, perfect for lightweight web applications.
  - It simplifies the setup process, as it doesn't require a separate database server, making it suitable for our small-scale Employee Portal.

- HTML:
  - HTML is the standard markup language used for creating the structure of web pages.
  - It's essential for defining the layout and content of the Employee Portal's user interface.

- CSS:
  - CSS (Cascading Style Sheets) is used to style and format the HTML elements on the web pages.
  - By using CSS, we can make the Employee Portal visually appealing and user-friendly.

## Features

- User Registration and Login: Job seekers and employers can create accounts and securely log in to the platform.
- Profile Creation and Management: Job seekers can build and update their portfolios, tailoring them to market requirements. Employers can create and manage their company profiles, showcasing their brand and values.
- Job Posting and Browsing: Employers can post job offers, including comprehensive details such as job descriptions, requirements, and application deadlines. Job seekers can easily search and browse available job offers based on their preferences and qualifications.
- Application Submission: Job seekers can apply for job offers by submitting their resumes and tailored cover letters, demonstrating their suitability for the position.
- Candidate Selection and Interview Management: Employers can review applications and select candidates for interviews. Both employers and job seekers receive notifications to stay informed throughout the hiring process.
- Job Recommendations: The platform includes a job recommendation system that suggests relevant job offers to job seekers based on their skills, experience, and preferences.
- Messaging and Communication: The platform provides a messaging system that allows job seekers and employers to communicate with each other, facilitating the interview scheduling and information exchange process.
- Notifications: Users receive notifications for various activities such as application status updates, interview invitations, and new job postings.
- Responsive User Interface: The user interface is designed to be responsive and accessible across different devices, ensuring a seamless user experience on desktops, tablets, and mobile devices.
- Analytics and Reporting: The platform includes analytics and reporting features that provide insights into application statistics, job posting performance, and user engagement, helping employers make data-driven decisions.

