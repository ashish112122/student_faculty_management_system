@echo off
echo ========================================
echo Verify Database Setup
echo ========================================
echo.

echo Connecting to Oracle and checking tables...
echo.

sqlplus -S system/Vanshi@Oracle1@localhost:1521/XE << EOF
SET PAGESIZE 50
SET LINESIZE 100

PROMPT ========================================
PROMPT Checking Tables
PROMPT ========================================

SELECT table_name FROM user_tables 
WHERE table_name IN ('USERS', 'STUDENTS', 'SUBJECTS', 'STUDENT_SUBJECTS', 
                     'FEEDBACK', 'FACULTY', 'MARKS', 'ATTENDANCE', 'ALERTS')
ORDER BY table_name;

PROMPT
PROMPT ========================================
PROMPT Checking Record Counts
PROMPT ========================================

SELECT 'USERS' as TABLE_NAME, COUNT(*) as RECORD_COUNT FROM users
UNION ALL
SELECT 'STUDENTS', COUNT(*) FROM students
UNION ALL
SELECT 'FACULTY', COUNT(*) FROM faculty
UNION ALL
SELECT 'SUBJECTS', COUNT(*) FROM subjects
UNION ALL
SELECT 'STUDENT_SUBJECTS', COUNT(*) FROM student_subjects
UNION ALL
SELECT 'MARKS', COUNT(*) FROM marks
UNION ALL
SELECT 'ATTENDANCE', COUNT(*) FROM attendance
UNION ALL
SELECT 'ALERTS', COUNT(*) FROM alerts
UNION ALL
SELECT 'FEEDBACK', COUNT(*) FROM feedback;

PROMPT
PROMPT ========================================
PROMPT Sample Student Data
PROMPT ========================================

SELECT name, email, role FROM users WHERE ROWNUM <= 5;

PROMPT
PROMPT ========================================
PROMPT Verification Complete!
PROMPT ========================================

EXIT;
EOF

echo.
pause
