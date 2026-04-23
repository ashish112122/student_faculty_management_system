"""
Member 2 — Faculty & Marks Module (RAHUL branch)
Flask Blueprint: faculty

Owns:   faculty table
Reads:  users, students, subjects (SELECT only)
Never modifies: users, students, subjects, student_subjects,
                feedback, attendance, alerts

Oracle DB via oracledb (python-oracledb).
Install: pip install oracledb
"""

from flask import Blueprint, request, jsonify
import oracledb
import os

faculty_bp = Blueprint("faculty", __name__)


# ---------------------------------------------------------------------------
# DB helper
# ---------------------------------------------------------------------------

def get_db():
    """Return an Oracle connection. Uses Thin mode (no Oracle Client needed)."""
    mode = oracledb.AUTH_MODE_SYSDBA if os.getenv("DB_MODE") == "sysdba" else oracledb.AUTH_MODE_DEFAULT
    return oracledb.connect(
        user=os.getenv("DB_USER", "sys"),
        password=os.getenv("DB_PASSWORD", "oracle"),
        dsn=os.getenv("DB_DSN", "localhost/XEPDB1"),
        mode=mode,
    )


def row_to_dict(cursor, row):
    """Convert an Oracle row tuple to a dict using cursor.description."""
    return {col[0].lower(): val for col, val in zip(cursor.description, row)}


def rows_to_list(cursor, rows):
    return [row_to_dict(cursor, r) for r in rows]


# ---------------------------------------------------------------------------
# Shared grade utility (imported by marks.py too)
# ---------------------------------------------------------------------------

def derive_grade(marks: float) -> str:
    """Return letter grade for a marks_obtained value in [0, 100]."""
    if marks >= 90:
        return "A"
    if marks >= 75:
        return "B"
    if marks >= 60:
        return "C"
    if marks >= 45:
        return "D"
    return "F"


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@faculty_bp.route("/faculty/profile/<int:faculty_id>", methods=["GET"])
def get_profile(faculty_id):
    """Return faculty profile for the given faculty_id."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "SELECT faculty_id, name, email, dept_id, designation "
            "FROM faculty WHERE faculty_id = :1",
            [faculty_id],
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Faculty not found"}), 404
        return jsonify(row_to_dict(cursor, row)), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()


@faculty_bp.route("/faculty/profile/update", methods=["POST"])
def update_profile():
    """Update dept_id and designation for a faculty member."""
    data        = request.get_json(silent=True) or {}
    faculty_id  = data.get("faculty_id")
    dept_id     = data.get("dept_id")
    designation = data.get("designation")

    if faculty_id is None or dept_id is None or designation is None:
        return jsonify({"error": "Missing required field: faculty_id, dept_id, designation"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        # Existence check — SELECT only on faculty
        cursor.execute(
            "SELECT faculty_id FROM faculty WHERE faculty_id = :1",
            [faculty_id],
        )
        if not cursor.fetchone():
            return jsonify({"error": "Faculty not found"}), 404

        # Write only to faculty table
        cursor.execute(
            "UPDATE faculty SET dept_id = :1, designation = :2 WHERE faculty_id = :3",
            [dept_id, designation, faculty_id],
        )
        db.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception:
        db.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()


@faculty_bp.route("/faculty/dashboard", methods=["GET"])
def dashboard():
    """
    Return faculty profile + class summary.
    Reads: faculty (profile), marks + subjects (class summary) — SELECT only.
    """
    faculty_id = request.args.get("faculty_id", type=int)
    if faculty_id is None:
        return jsonify({"error": "Missing required query param: faculty_id"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        # Profile — SELECT on faculty only
        cursor.execute(
            "SELECT faculty_id, name, email, dept_id, designation "
            "FROM faculty WHERE faculty_id = :1",
            [faculty_id],
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Faculty not found"}), 404
        profile = row_to_dict(cursor, row)

        # Class summary — SELECT on marks JOIN subjects (read-only)
        cursor.execute(
            """
            SELECT m.subject_id,
                   s.subject_name,
                   COUNT(DISTINCT m.student_id) AS student_count
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE s.faculty_id = :1
            GROUP BY m.subject_id, s.subject_name
            """,
            [faculty_id],
        )
        classes = rows_to_list(cursor, cursor.fetchall())

        return jsonify({"profile": profile, "classes": classes}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
