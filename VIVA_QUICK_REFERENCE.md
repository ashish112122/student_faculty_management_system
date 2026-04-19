# VIVA QUICK REFERENCE GUIDE
## Student-Faculty Management System

---

## 🎯 PROJECT AT A GLANCE

**Name:** Student-Faculty Management System (SFMS)
**Database:** Oracle 21c Express Edition
**Backend:** Python Flask
**Frontend:** HTML5, CSS3, JavaScript, Chart.js
**Authentication:** JWT (JSON Web Tokens)

---

## 📊 DATABASE STATISTICS

| Item | Count |
|------|-------|
| Total Tables | 11 (9 main + 2 junction) |
| Primary Keys | 11 |
| Foreign Keys | 15+ |
| Triggers | 1 |
| Sequences | 9 |
| Indexes | 5 |
| API Endpoints | 25+ |
| SQL Queries | 50+ |

---

## 📋 ALL TABLES

1. **users** - Login credentials (student + faculty)
2. **students** - Student information
3. **faculty** - Faculty information
4. **subjects** - Course information
5. **marks** - Academic performance
6. **attendance** - Daily attendance
7. **alerts** - System notifications
8. **feedback_threads** - Conversation metadata
9. **feedback_messages** - Chat messages
10. **student_subjects** - Student-Subject mapping (M:N)
11. **faculty_classes** - Faculty-Subject-Class mapping (M:N)

---

## 🔗 RELATIONSHIPS

| From | To | Type | Example |
|------|-----|------|---------|
| users | students | 1:1 | One user = one student |
| users | faculty | 1:1 | One user = one faculty |
| students | marks | 1:N | One student has many marks |
| students | attendance | 1:N | One student has many attendance records |
| students | alerts | 1:N | One student has many alerts |
| students | subjects | M:N | Many students enroll in many subjects |
| faculty | subjects | M:N | Many faculty teach many subjects |
| students | faculty | M:N | Many students chat with many faculty |

---

## ⚙️ KEY FEATURES

### Student Portal:
✅ View marks with charts
✅ View attendance with percentage
✅ View alerts (low attendance warnings)
✅ Chat with faculty
✅ Clear chat history

### Faculty Portal:
✅ Enter/update marks
✅ Mark attendance (P/A)
✅ Chat with students
✅ View unread messages
✅ Batch-based management

### System Features:
✅ Automated attendance alerts (< 75%)
✅ Real-time messaging
✅ JWT authentication
✅ Transaction management

---

## 📐 NORMALIZATION

**Level:** BCNF (Boyce-Codd Normal Form)

**1NF:** ✅ All atomic values, no repeating groups
**2NF:** ✅ No partial dependencies
**3NF:** ✅ No transitive dependencies
**BCNF:** ✅ All determinants are candidate keys

---

## 🔔 ATTENDANCE ALERT SYSTEM

| Attendance % | Alert Type | Color |
|--------------|------------|-------|
| 75% - 100% | None | Green |
| 65% - 75% | Warning | Yellow |
| 50% - 65% | Alert | Orange |
| Below 50% | Critical | Red |

**Formula:** `Percentage = (Present Days / Total Days) × 100`

---

## 📝 MARKS DISTRIBUTION

| Assessment | Maximum Marks |
|------------|---------------|
| MST (Mid Semester Test) | 30 |
| EST (End Semester Test) | 40 |
| Quiz | 15 |
| Assignment | 15 |
| **Total** | **100** |

---

## 🔧 TRIGGER EXPLANATION

**Name:** `update_thread_timestamp`

**When:** AFTER INSERT on feedback_messages

**What:** Automatically updates `last_message_at` in feedback_threads

**Why:** Keeps conversation list sorted by recent activity

**Code:**
```sql
CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
```

---

## 💾 SQL OPERATIONS USED

### DDL (Data Definition Language):
- CREATE TABLE
- CREATE SEQUENCE
- CREATE INDEX
- CREATE TRIGGER
- PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL

### DML (Data Manipulation Language):
- SELECT (simple, with WHERE, ORDER BY, DISTINCT)
- INSERT
- UPDATE
- DELETE
- JOIN (INNER, LEFT, multiple tables)
- Aggregate Functions (COUNT, SUM, AVG, MAX)
- GROUP BY
- HAVING
- Subqueries (scalar, correlated)
- EXISTS operator

---

## 🎓 COMMON VIVA QUESTIONS & ANSWERS

### Q1: What is the objective of your project?
**A:** To create a digital platform for managing student-faculty interactions, tracking academic performance (marks and attendance), and facilitating communication through a real-time chat system.

### Q2: Why did you choose Oracle Database?
**A:** Oracle is an enterprise-grade RDBMS that supports ACID properties, provides automatic recovery mechanisms, handles concurrent users efficiently, and is required for our DBMS course curriculum.

### Q3: What normalization level is your database in?
**A:** Our database is normalized up to BCNF (Boyce-Codd Normal Form). All tables have atomic values (1NF), no partial dependencies (2NF), no transitive dependencies (3NF), and all determinants are candidate keys (BCNF).

### Q4: Explain how the attendance alert system works.
**A:** 
1. Faculty marks attendance (P or A)
2. System calculates percentage: (Present/Total) × 100
3. If percentage < 75%, alert is generated
4. Alert type determined: Warning (65-75%), Alert (50-65%), Critical (<50%)
5. Alert inserted into database
6. Student sees alert in portal

### Q5: What is the purpose of the trigger in your project?
**A:** The `update_thread_timestamp` trigger automatically updates the `last_message_at` field in the feedback_threads table whenever a new message is inserted. This keeps the conversation list sorted by most recent activity without manual updates.

### Q6: Explain the relationships in your database.
**A:** 
- **1:1** - User to Student, User to Faculty (via user_id)
- **1:N** - Student to Marks, Student to Attendance, Student to Alerts
- **M:N** - Student to Subject (via student_subjects), Faculty to Subject (via faculty_classes), Student to Faculty (via feedback_threads)

### Q7: How does JWT authentication work?
**A:**
1. User enters credentials
2. Backend validates against database
3. If valid, generates JWT token with user_id and role
4. Token sent to frontend
5. Frontend stores in localStorage
6. Every API request includes token in header
7. Backend validates token before processing request

### Q8: What are the main features of your system?
**A:**
- **For Students:** View marks, view attendance, receive alerts, chat with faculty
- **For Faculty:** Enter marks, mark attendance, chat with students, manage batches
- **System:** Automated alerts, real-time messaging, transaction management

### Q9: How do you ensure data integrity?
**A:**
- Primary keys for unique identification
- Foreign keys for referential integrity
- CHECK constraints for valid values
- NOT NULL constraints for required fields
- UNIQUE constraints for unique values
- Transaction management (COMMIT/ROLLBACK)

### Q10: What SQL queries are most complex in your project?
**A:** The attendance alert query with GROUP BY and HAVING:
```sql
SELECT s.student_id, sub.subject_name,
       COUNT(*) as total,
       SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
FROM students s
JOIN attendance a ON s.student_id = a.student_id
JOIN subjects sub ON a.subject_id = sub.subject_id
GROUP BY s.student_id, sub.subject_name
HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75;
```

---

## 🚀 PROJECT FLOW

```
Login → Authentication → Dashboard → Feature Selection → Data Operations → Response
```

**Detailed:**
1. User opens login page
2. Enters email and password
3. Backend validates credentials
4. Generates JWT token
5. Redirects to appropriate portal
6. Loads dashboard data
7. User selects feature (Marks/Attendance/Feedback/Alerts)
8. Makes API request
9. Backend queries database
10. Returns JSON response
11. Frontend displays data

---

## 📱 DEMO CREDENTIALS

**Students:**
- rohan.sharma@thapar.edu / password123
- priya.singh@thapar.edu / password123

**Faculty:**
- rohan.sharma@thaparfac.edu / password123
- neha.verma@thaparfac.edu / password123

---

## ✅ PROJECT COMPLETION CHECKLIST

- [x] Database design (11 tables)
- [x] Normalization (BCNF)
- [x] Primary and foreign keys
- [x] Triggers (1 trigger)
- [x] Sequences (9 sequences)
- [x] Indexes (5 indexes)
- [x] Backend API (25+ endpoints)
- [x] Frontend UI (3 pages)
- [x] Authentication (JWT)
- [x] CRUD operations
- [x] Joins (INNER, LEFT)
- [x] Aggregate functions
- [x] GROUP BY and HAVING
- [x] Subqueries
- [x] Transaction management
- [x] Error handling
- [x] Testing and debugging

---

**Status:** ✅ Complete and Production Ready
**Documentation:** ✅ Comprehensive
**Viva Preparation:** ✅ Ready

---

**For detailed explanation, refer to:** `VIVA_DOCUMENTATION_COMPLETE.md`
