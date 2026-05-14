# Student Management System

A modern Flask-based Student Management System with authentication, authorization, REST APIs, and SQLite database integration.

---

# Features

## Student Management
- Add students
- Edit student details
- Delete students
- Search students
- View all students

## Authentication System
- User signup
- User login
- User logout
- Session handling
- Protected routes
- Flash messages

## Security Features
- Password hashing using Werkzeug
- Role-based authorization
- Admin-only actions
- Authentication decorators

## REST APIs
- API signup/login/logout
- API dashboard
- API add/update/delete student
- API search students
- JSON responses
- Proper status codes

## Frontend
- Responsive UI
- Modern glassmorphism design
- Dashboard page
- Login & signup pages

---

# Tech Stack

- Python
- Flask
- SQLite3
- HTML
- CSS

---

# Project Structure
student-manager/
│
├── app.py
├── students.db
├── README.md
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── edit.html
│
├── static/
│   └── style.css


Authentication & Authorization

The project includes:

Session-based authentication
Role-based authorization
Admin-only access for edit/delete operations
Reusable decorators:
login_required
admin_required
REST API Endpoints
Method	Endpoint	Description
POST	/api/signup	Register user
POST	/api/login	Login user
POST	/api/logout	Logout user
GET	/api/dashboard	Dashboard stats
GET	/api/search-students	Search students
DELETE	/api/delete-student/<id>	Delete student
PUT	/api/update-student/<id>	Update student
Installation
1. Clone Repository
git clone https://github.com/Bhavan-12/student-manager.git
2. Install Flask
pip install flask
3. Run Application
python app.py
4. Open Browser
http://127.0.0.1:5000
Future Improvements
Deployment
Better API structure
JWT Authentication
User profile system
Pagination
Better dashboard analytics
React frontend integration
What I Learned

Through this project I learned:

Flask fundamentals
CRUD operations
SQLite integration
Sessions & authentication
Password hashing
REST APIs
Role-based authorization
Decorators
Backend architecture basics
Git & GitHub workflow
