import oracledb
import sys
sys.path.append('backend')
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

# Get a student and subject
cursor.execute("SELECT student_id FROM students WHERE ROWNUM = 1")
student_id = cursor.fetchone()[0]
cursor.execute("SELECT subject_id FROM subjects WHERE ROWNUM = 1")
subject_id = cursor.fetchone()[0]

# Current attendance percentage
cursor.execute("""
    SELECT COUNT(*), SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END)
    FROM attendance WHERE student_id = :s AND subject_id = :sub
""", {'s': student_id, 'sub': subject_id})
row = cursor.fetchone()
total, present = row[0], (row[1] or 0)
pct = round((present / total) * 100, 2) if total else 0
print(f"Student {student_id}, Subject {subject_id}: {present}/{total} = {pct}%")

# Alerts before
cursor.execute("SELECT COUNT(*) FROM alerts WHERE student_id = :s AND subject_id = :sub",
               {'s': student_id, 'sub': subject_id})
before = cursor.fetchone()[0]
print(f"Alerts before: {before}")

# Verify triggers
cursor.execute("SELECT trigger_name, table_name, triggering_event, status FROM user_triggers ORDER BY trigger_name")
print("\nTriggers in database:")
print("-" * 60)
for r in cursor.fetchall():
    print(f"  {r[0]:<35} | {r[1]:<20} | {r[2]:<20} | {r[3]}")

# Verify SQL-based attendance percentage matches Python calculation
cursor.execute("""
    SELECT ROUND(SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2)
    FROM attendance
    WHERE student_id = :s AND subject_id = :sub
""", {'s': student_id, 'sub': subject_id})
sql_pct = cursor.fetchone()[0]
print(f"\nSQL-calculated percentage: {sql_pct}%")
print("Attendance percentage is now calculated entirely in SQL.")

cursor.close()
conn.close()
