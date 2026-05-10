from flask import Flask, jsonify, render_template, request, redirect, jsonify, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            branch TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    
    search = request.args.get("search")
    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{search}%",))
    else:
        cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    if not students:
        message = "No students found"
    else:
        if len(students) == 1:
            message = "1 student found"
        else:
            message = f"{len(students)} students found"

    conn.close()
    return render_template("index.html", students=students, message=message)


@app.route("/add-student", methods=["POST"])
def add_student():
    name = request.form.get("name")
    branch = request.form.get("branch")

    if not name or not branch:
        return "Name and branch are required"

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    existing_student = cursor.fetchone()

    if existing_student:
        conn.close()
        return "Student already exists"

    cursor.execute(
        "INSERT INTO students (name, branch) VALUES (?, ?)",
        (name, branch)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("edit.html", student=student)

@app.route("/update/<int:student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form.get("name")
    branch = request.form.get("branch")

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name = ?, branch = ? WHERE id = ?",
        (name, branch, student_id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/api/student/<int:student_id>")
def api_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    conn.close()

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"id": student[0], "name": student[1], "branch": student[2]})

@app.route("/api/students")
def api_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    students_list = [{"id": student[0], "name": student[1], "branch": student[2]} for student in students]

    return jsonify(students_list)
@app.route("/api/add-student", methods = ["POST"])
def api_add_student():
    data =  request.get.json()
    name = data.get("name")
    branch = data.get("branch")
    if not name or not branch:
        return jsonify ({"error": "name and branch are required"}), 400
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
    existing_student = cursor.fetchone()
    if existing_student:
        conn.close()
        return jsonify({"error": "Student already exists"}), 400
    cursor.execute(
        "INSERT INTO students (name, branch) VALUES (?, ?)",
        (name, branch)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201
@app.route("/signup-page")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "username and password are required", 400

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        flash("user already exists")
        return redirect("/signup-page")

    hashed_password = generate_password_hash(password)

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed_password)
    )

    conn.commit()
    conn.close()

    session["user"] = username

    return redirect("/dashboard")

@app.route("/login-page")
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Username and password are required", 400

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        flash("Invalid credentials")
        return redirect("/login-page")
    
    if not check_password_hash(user[2], password):
        flash("Invalid credentials")
        return redirect("/login-page")

    session["user"] = username
    return render_template("dashboard.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first")
        return redirect("/login-page")

    return render_template("dashboard.html")  
 
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login-page")
 

if __name__ == "__main__":
    app.run(debug=True)