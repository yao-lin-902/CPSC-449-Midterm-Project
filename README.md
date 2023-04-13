# CPSC-449-Midterm-Project
Team Members: Yao Lin, Arish Imam, Karnikaa Velumani

Back End Project

A simple web app using Flask, MySQL, Flask-JWT-Extended, and Flask-Bcrypt to create a user registration and login system, as well as displaying public items.

Requirements:

Python 3.6+
Flask
Flask-Bcrypt
Flask-JWT-Extended
Flask-MySQLDB
Flask-CORS
WTForms


Installation:

Clone the repository or download the source code.
Install the required packages using pip install -r requirements.txt.
Create a MySQL database named web and create the tables user and public_items with the appropriate schema.
Update the app.config["MYSQL_*"] variables with your MySQL database credentials in the app.py file.
Run the app using python app.py and access it on http://localhost:5000.

Features:

User registration, login, and logout
Password hashing using Flask-Bcrypt
JWT authentication with access tokens stored in cookies
Profile page with the option to upload a profile picture
A public route to display publicly viewable items from the public_items table

Structure:

The application's structure is as follows:

app.py: Main application file with routes and helper functions.
templates: Contains the HTML templates for the web app.
static: Contains static files such as images.
error-pages: Contains error pages for specific HTTP status codes (e.g., 404, 401).

Routes:

/: Home page
/home: Home page (alias)
/login: User login
/register: User registration
/logout: User logout
/profile: User profile page (protected)
/upload_profile_pic: Profile picture upload (protected)
/public: Public route to display publicly viewable items