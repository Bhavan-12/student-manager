from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


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

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def index():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return render_template("index.html", students=students)


@app.route("/add-student", methods=["POST"])
def add_student():
    name = request.form.get("name")
    branch = request.form.get("branch")

    if not name or not branch:
        return "Name and branch are required"

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

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

if __name__ == "__main__":
    app.run(debug=True)