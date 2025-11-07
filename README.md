Elite Tourism - Dynamic Web Application

(Suggestion: Replace the placeholder above with a real screenshot of your running application!)

1. Project Description

Elite Tourism is a sophisticated, database-driven web application designed as a fully functional Content Management System (CMS) for a luxury travel website. What began as a static HTML/CSS brochure has been rebuilt into a dynamic site powered by a Python and Flask backend.

The application supports two distinct user roles:

Normal Users: Can browse states, view cities within those states, and see detailed descriptions of each location.

Admin User: Can log in to a secure, protected control panel to manage all website content.

The core of this project is the admin's ability to perform CRUD (Create, Read, Update, Delete) operations on all travel destinations, which are organized in a State -> City hierarchy.

2. Key Features

User Features

Dynamic Homepage: The homepage automatically displays all "States" (e.g., Gujarat, Maharashtra) from the database.

Hierarchical Navigation: Users can click a "State" to see all the "Cities" within it, and then click a "City" to see its full details page.

Secure Authentication: A complete user registration and login system (/login, /register).

User Dashboard: A simple, protected dashboard for logged-in users.

Fully Responsive: Designed with Tailwind CSS to work on mobile, tablet, and desktop.

Admin-Only Features

Protected Admin Panel: The /admin route and all sub-routes are protected and can only be accessed by the user with the is_admin flag.

Full "State" Management: Admins can add, edit, and delete states from a "Manage States" dashboard.

Full "City" Management: Admins can select a state, then add, edit, or delete cities that are automatically linked to that parent state.

Rich Text Details: The "Full Details" field for a city is rendered with | safe, allowing the admin to embed raw HTML, such as <img> tags or custom formatting, directly from the text box.

3. Technology Stack

Backend: Python (v3.13+), Flask

Database: Flask-SQLAlchemy with SQLite

Authentication: Flask-Login (for managing user sessions)

Frontend: HTML5, Tailwind CSS, modern JavaScript

Templating: Jinja2

4. Project Structure

Elite-Tourism-Project/
│
├── app.py             # The main Flask server (the "brain")
├── users.db           # The SQLite database (auto-generated)
│
├── templates/         # All .html files
│   ├── layout.html    # Base template (navbar, footer)
│   ├── index.html     # Homepage (shows states)
│   ├── state_detail.html
│   ├── city_detail.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html # User dashboard
│   ├── admin.html     # Admin control panel
│   ├── admin_states.html
│   ├── edit_state.html
│   ├── admin_cities.html
│   └── edit_city.html
│
└── static/            # All assets
    ├── style.css
    ├── script.js
    ├── images/        # All .jpg files for states/cities
    └── videos/        # All .mp4 files for backgrounds


5. Setup & Installation

To run this project on your local machine, follow these steps:

Clone the Repository

git clone [https://github.com/your-username/elite-tourism-project.git](https://github.com/your-username/elite-tourism-project.git)
cd elite-tourism-project


Create a Virtual Environment (Recommended)

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate


Install Dependencies
This project relies on Flask, Flask-SQLAlchemy, and Flask-Login.

pip install flask flask_sqlalchemy flask_login


Run the Application
When you run app.py for the first time, it will automatically create the users.db file and populate it with the admin account.

python app.py


Access the Site
Open your browser and go to: http://127.0.0.1:5000/

6. How to Use

Admin Account

The admin account is automatically created when you first run the server.

Email: admin@gmail.com

Password: Admin@123

Adding Your First State & City

Log in as the admin. You will be redirected to the "Admin Control Panel".

Add your images: Place your image files (e.g., state-gujarat.jpg) inside the static/images/ folder.

Go to "Manage States" and fill out the "Add New State" form. Use the exact filename (e.g., state-gujarat.jpg) in the "Image Filename" field.

Click the "Manage Cities" button on your new state.

On the "Manage Cities" page, add a new city. You can add embedded images in the "Full Details" box (e.g., <img src="https://example.com/image.jpg">).

Log out and go to the homepage. You will see your new content live!

7. Future Features

The next logical steps for this project are:

Activate the "Send Inquiry" Form: Create a new Inquiry table in the database to store user messages and build a "View Inquiries" page in the admin panel.

Password Hashing: Update the User model to hash and salt passwords instead of storing them as plain text.
