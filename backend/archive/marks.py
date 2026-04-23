"""
Member 2 — Faculty & Marks Module (RAHUL branch)
Flask Blueprint: marks

Owns:   marks table
Reads:  students, subjects (SELECT only for validation/joins)
Never modifies: users, students, subjects, student_subjects,
                feedback, attendance, alerts

Oracle DB via oracledb (python-oracledb).
Install: pip install oracledb
"""

from flask import Blueprint, request, jsonify
import oracledb

from backend.faculty import derive_grade, get_db, rows_to_list, row_to_dict

marks_bp = Blueprint("marks", __name__)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@marks_bp.route("/marks/add", methods=["POST"])
def add_marks():
    """Insert a new marks record after validation."""
    data           = request.get_json(silent=True) or {}
    student_id     = data.get("student_id")
    subject_id     = data.get("subject_id")
    marks_obtained = data.get("marks_obtained")
    exam_type      = data.get("exam_type")

    for field, val in [("student_id", student_id), ("subject_id", subject_id),
                       ("marks_obtained", marks_obtained), ("exam_type", exam_type)]:
        if val is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        marks_obtained = float(marks_obtained)
    except (TypeError, ValueError):
        return jsonify({"error": "marks_obtained must be a number"}), 400

    if not (0 <= marks_obtained <= 100):
        return jsonify({"error": "marks_obtained must be between 0 and 100"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        # Validate student_id — SELECT only on students
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE student_id = :1",
            [student_id],
        )
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Student not found"}), 404

        # Validate subject_id — SELECT only on subjects
        cursor.execute(
            "SELECT COUNT(*) FROM subjects WHERE subject_id = :1",
            [subject_id],
        )
        if cursor.fetchone()[0] == 0:
            return jsonify({"error": "Subject not found"}), 404

        grade = derive_grade(marks_obtained)

        # Retrieve the new marks_id via RETURNING INTO
        new_id_var = cursor.var(oracledb.NUMBER)
        cursor.execute(
            "INSERT INTO marks (student_id, subject_id, marks_obtained, grade, exam_type) "
            "VALUES (:1, :2, :3, :4, :5) RETURNING marks_id INTO :6",
            [student_id, subject_id, marks_obtained, grade, exam_type, new_id_var],
        )
        db.commit()
        new_id = int(new_id_var.getvalue()[0])
        return jsonify({"message": "Marks added", "marks_id": new_id}), 201
    except Exception:
        db.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()


@marks_bp.route("/marks/update/<int:marks_id>", methods=["PUT"])
def update_marks(marks_id):
    """Update marks_obtained and recalculate grade for an existing record."""
    data           = request.get_json(silent=True) or {}
    marks_obtained = data.get("marks_obtained")

    if marks_obtained is None:
        return jsonify({"error": "Missing required field: marks_obtained"}), 400

    try:
        marks_obtained = float(marks_obtained)
    except (TypeError, ValueError):
        return jsonify({"error": "marks_obtained must be a number"}), 400

    if not (0 <= marks_obtained <= 100):
        return jsonify({"error": "marks_obtained must be between 0 and 100"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        # Existence check — SELECT on marks
        cursor.execute(
            "SELECT marks_id FROM marks WHERE marks_id = :1",
            [marks_id],
        )
        if not cursor.fetchone():
            return jsonify({"error": "Marks record not found"}), 404

        grade = derive_grade(marks_obtained)

        # Write only to marks table
        cursor.execute(
            "UPDATE marks SET marks_obtained = :1, grade = :2 WHERE marks_id = :3",
            [marks_obtained, grade, marks_id],
        )
        db.commit()
        return jsonify({"message": "Marks updated", "grade": grade}), 200
    except Exception:
        db.rollback()
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()


@marks_bp.route("/marks/results", methods=["GET"])
def get_results():
    """Return all marks for a subject + exam_type, sorted by marks DESC."""
    subject_id = request.args.get("subject_id", type=int)
    exam_type  = request.args.get("exam_type", type=str)

    if subject_id is None or not exam_type:
        return jsonify({"error": "Missing required query params: subject_id, exam_type"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT m.marks_id,
                   st.name       AS student_name,
                   su.subject_name,
                   m.marks_obtained,
                   m.grade,
                   m.exam_type
            FROM marks m
            JOIN students st ON m.student_id = st.student_id
            JOIN subjects su ON m.subject_id = su.subject_id
            WHERE m.subject_id = :1 AND m.exam_type = :2
            ORDER BY m.marks_obtained DESC
            """,
            [subject_id, exam_type],
        )
        rows = rows_to_list(cursor, cursor.fetchall())
        return jsonify(rows), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()


@marks_bp.route("/marks/chart-data", methods=["GET"])
def chart_data():
    """Return student_name + marks_obtained for Chart.js rendering."""
    subject_id = request.args.get("subject_id", type=int)
    exam_type  = request.args.get("exam_type", type=str)

    if subject_id is None or not exam_type:
        return jsonify({"error": "Missing required query params: subject_id, exam_type"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            SELECT st.name AS student_name, m.marks_obtained
            FROM marks m
            JOIN students st ON m.student_id = st.student_id
            WHERE m.subject_id = :1 AND m.exam_type = :2
            """,
            [subject_id, exam_type],
        )
        rows = rows_to_list(cursor, cursor.fetchall())
        return jsonify(rows), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        cursor.close()
        db.close()



@marks_bp.route("/marks/analytics", methods=["GET"])
def analytics():
    subject_id = request.args.get("subject_id", type=int)
    exam_type  = request.args.get("exam_type", type=str)
    if subject_id is None or not exam_type:
        return jsonify({"error": "Missing required query params: subject_id, exam_type"}), 400
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """SELECT m.marks_id, st.name AS student_name, m.marks_obtained, m.grade
               FROM marks m JOIN students st ON m.student_id = st.student_id
               WHERE m.subject_id = :1 AND m.exam_type = :2
               ORDER BY m.marks_obtained DESC""",
            [subject_id, exam_type]
        )
        rows = rows_to_list(cursor, cursor.fetchall())
        if not rows:
            return jsonify({"error": "No data found"}), 404
        marks_list = [r["marks_obtained"] for r in rows]
        n = len(marks_list)
        avg = sum(marks_list) / n
        sorted_marks = sorted(marks_list)
        mid = n // 2
        median = (sorted_marks[mid] if n % 2 != 0 else (sorted_marks[mid-1] + sorted_marks[mid]) / 2)
        grade_dist = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for r in rows:
            g = r["grade"] or "F"
            if g in grade_dist:
                grade_dist[g] += 1
        return jsonify({
            "students": rows,
            "stats": {"average": round(avg,2), "median": round(median,2), "highest": max(marks_list), "lowest": min(marks_list), "total": n},
            "grade_distribution": grade_dist,
            "at_risk": [r for r in rows if r["marks_obtained"] < 45],
            "top_performers": [r for r in rows if r["marks_obtained"] >= 75],
        }), 200
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
