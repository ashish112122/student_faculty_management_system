"""
Main Flask app — Member 2 (Faculty & Marks module)
Registers faculty_bp and marks_bp, serves HTML templates.
"""

from flask import Flask, render_template, session, redirect, url_for
from dotenv import load_dotenv
import os
load_dotenv()

from backend.faculty import faculty_bp
from backend.marks import marks_bp

app = Flask(__name__, template_folder="templates", static_folder="frontend", static_url_path="/static")
app.secret_key = os.getenv("SECRET_KEY", "change-me-in-production")

app.register_blueprint(faculty_bp)
app.register_blueprint(marks_bp)


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("faculty_dashboard.html", faculty_id=session.get("faculty_id", 1))


@app.route("/my_classes")
def my_classes_page():
    faculty_id = session.get("faculty_id", 1)
    return render_template("my_classes.html", faculty_id=faculty_id)


@app.route("/add_marks")
def add_marks_page():
    return render_template("add_marks.html")


@app.route("/marks_report")
def marks_report_page():
    return render_template("marks_report.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
