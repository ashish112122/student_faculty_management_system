# Team Integration Guide

## For Team Members 2 & 3

### Database Tables You Can Use

**Available Tables (Created by Member 1):**
- `users` - All user credentials and basic info
- `students` - Student profile data
- `subjects` - Subject information
- `student_subjects` - Student enrollment mapping

### Tables You Need to Create

**Member 2 (Faculty & Marks):**
- `faculty` - Faculty profile information
- `marks` - Student marks (MST, EST, Assignment, Quiz)

**Member 3 (Attendance & Alerts):**
- `attendance` - Daily attendance records
- `alerts` - Auto-generated alerts

### API Integration Points

**Member 2 - Add these endpoints:**
```
POST /api/faculty/marks - Add/update marks
GET /api/faculty/students - Get student list
```

**Member 3 - Add these endpoints:**
```
POST /api/faculty/attendance - Mark attendance
GET /api/faculty/attendance - View attendance
```

### Naming Convention
- Use **snake_case** for all table names
- Use **snake_case** for all column names
- Follow existing patterns in schema.sql

### Foreign Key References
```sql
-- Reference students
FOREIGN KEY (student_id) REFERENCES students(student_id)

-- Reference subjects
FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)

-- Reference users
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

### Merge Strategy
1. Each member works on separate branch
2. No overlapping files
3. Database schema is additive (no conflicts)
4. API routes are independent
5. Frontend pages are separate

### File Ownership

**Member 1 Files (DO NOT MODIFY):**
- frontend/login.html
- frontend/dashboard.html
- frontend/marks.html
- frontend/attendance.html
- frontend/alerts.html
- frontend/feedback.html
- backend/app.py (routes for student module)

**Member 2 Should Create:**
- frontend/faculty-marks.html
- backend/routes/faculty_routes.py
- backend/routes/marks_routes.py

**Member 3 Should Create:**
- frontend/faculty-attendance.html
- backend/routes/attendance_routes.py
- backend/utils/alert_scheduler.py

### Testing Your Integration
1. Run schema.sql first
2. Run demo_data.sql
3. Start Flask backend
4. Test your endpoints
5. Verify no conflicts with existing tables
