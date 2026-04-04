# API Reference - Student-Faculty Portal v2.0

Base URL: `http://localhost:5000`

## Authentication

All endpoints except `/api/login` require JWT token in Authorization header:
```
Authorization: Bearer <token>
```

### POST /api/login
Login to the system

**Request Body:**
```json
{
  "email": "rohan.sharma.2q11@thapar.edu",
  "password": "pass123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 11,
  "name": "Rohan Sharma",
  "role": "student",
  "student_id": 1,
  "class_name": "2Q11",
  "message": "Login successful"
}
```

---

## Student Endpoints

### GET /api/student/dashboard
Get student profile and overview

**Response:**
```json
{
  "name": "Rohan Sharma",
  "branch": "Computer Engineering",
  "year": 2,
  "semester": 4,
  "class_name": "2Q11",
  "cgpa": 8.5,
  "subjects": [
    {"name": "Database Management Systems", "code": "CS301"},
    {"name": "Operating Systems", "code": "CS302"}
  ]
}
```

### GET /api/student/subjects
Get list of enrolled subjects

**Response:**
```json
[
  {
    "subject_id": 1,
    "subject_name": "Database Management Systems",
    "subject_code": "CS301"
  }
]
```

### GET /api/student/marks?subject_id={id}
Get marks for a specific subject

**Response:**
```json
[
  {
    "assessment_type": "MST",
    "marks_obtained": 38,
    "max_marks": 50,
    "class_average": 35.5
  },
  {
    "assessment_type": "EST",
    "marks_obtained": 72,
    "max_marks": 100,
    "class_average": 68.2
  }
]
```

### GET /api/student/attendance?subject_id={id}
Get attendance for a specific subject

**Response:**
```json
{
  "percentage": 85.5,
  "present": 60,
  "total": 70,
  "records": [
    {"date": "2026-04-04", "status": "Present"},
    {"date": "2026-04-03", "status": "Absent"}
  ]
}
```

### GET /api/student/alerts
Get all alerts for the student

**Response:**
```json
[
  {
    "alert_type": "Warning",
    "message": "Low attendance in Operating Systems: 72% (50/70 classes)",
    "created_at": "2026-04-01 10:30",
    "subject": "Operating Systems"
  }
]
```

### GET /api/student/feedback/threads
Get all feedback threads (subjects with messages)

**Response:**
```json
[
  {
    "subject_id": 1,
    "subject_name": "Database Management Systems",
    "subject_code": "CS301",
    "message_count": 5,
    "last_message_time": "2026-04-04 14:30"
  }
]
```

### GET /api/student/feedback?subject_id={id}
Get full conversation thread for a subject

**Response:**
```json
{
  "messages": [
    {
      "message": "I have a doubt about normalization",
      "timestamp": "2026-04-04 10:00:00",
      "sender_name": "Rohan Sharma",
      "sender_role": "student",
      "is_own_message": true
    },
    {
      "message": "Sure, what specific aspect would you like to discuss?",
      "timestamp": "2026-04-04 10:15:00",
      "sender_name": "Dr. Rajesh Kumar",
      "sender_role": "faculty",
      "is_own_message": false
    }
  ],
  "faculty": {
    "user_id": 1,
    "name": "Dr. Rajesh Kumar",
    "faculty_id": 1
  }
}
```

### POST /api/student/feedback
Send a message to faculty

**Request Body:**
```json
{
  "subject_id": 1,
  "message": "I have a doubt about normalization"
}
```

**Response:**
```json
{
  "message": "I have a doubt about normalization",
  "timestamp": "2026-04-04 10:00:00",
  "sender_name": "Rohan Sharma",
  "sender_role": "student",
  "is_own_message": true
}
```

---

## Faculty Endpoints

### GET /api/faculty/dashboard
Get faculty profile and overview

**Response:**
```json
{
  "name": "Dr. Rajesh Kumar",
  "department": "Computer Science",
  "designation": "Associate Professor",
  "classes": ["2Q11", "2Q12", "2Q13"],
  "total_students": 90
}
```

### GET /api/faculty/classes
Get all classes taught by faculty

**Response:**
```json
[
  {
    "class_name": "2Q11",
    "student_count": 30
  },
  {
    "class_name": "2Q12",
    "student_count": 30
  }
]
```

### GET /api/faculty/class/students?class_name={name}
Get all students in a specific class

**Response:**
```json
[
  {
    "student_id": 1,
    "name": "Rohan Sharma",
    "email": "rohan.sharma.2q11@thapar.edu",
    "cgpa": 8.5
  }
]
```

### GET /api/faculty/subjects?class_name={name}
Get subjects taught for a specific class (optional parameter)

**Response:**
```json
[
  {
    "subject_id": 1,
    "subject_name": "Database Management Systems",
    "subject_code": "CS301"
  }
]
```

### GET /api/faculty/marks?class_name={name}&subject_id={id}
Get marks for all students in a class for a subject

**Response:**
```json
[
  {
    "student_id": 1,
    "name": "Rohan Sharma",
    "marks": [
      {
        "assessment_type": "MST",
        "marks_obtained": 38,
        "max_marks": 50
      }
    ]
  }
]
```

### POST /api/faculty/marks
Add or update marks for a student

**Request Body:**
```json
{
  "class_name": "2Q11",
  "subject_id": 1,
  "student_id": 1,
  "assessment_type": "MST",
  "marks_obtained": 38,
  "max_marks": 50
}
```

**Response:**
```json
{
  "message": "Marks saved successfully"
}
```

### GET /api/faculty/marks/report?class_name={name}&subject_id={id}
Get marks statistics for a class

**Response:**
```json
[
  {
    "assessment_type": "MST",
    "highest": 48,
    "lowest": 25,
    "average": 36.5,
    "max_marks": 50
  },
  {
    "assessment_type": "EST",
    "highest": 92,
    "lowest": 45,
    "average": 71.2,
    "max_marks": 100
  }
]
```

### GET /api/faculty/attendance?class_name={name}&subject_id={id}&date={date}
Get attendance for a class (with optional date parameter)

**Without date (summary):**
```json
[
  {
    "student_id": 1,
    "name": "Rohan Sharma",
    "total_classes": 70,
    "present_count": 60,
    "percentage": 85.71
  }
]
```

**With date (specific day):**
```json
[
  {
    "student_id": 1,
    "name": "Rohan Sharma",
    "status": "P"
  }
]
```

### POST /api/faculty/attendance
Mark attendance for students

**Request Body:**
```json
{
  "class_name": "2Q11",
  "subject_id": 1,
  "date": "2026-04-04",
  "attendance": [
    {"student_id": 1, "status": "P"},
    {"student_id": 2, "status": "A"}
  ]
}
```

**Response:**
```json
{
  "message": "Attendance marked successfully"
}
```

### GET /api/faculty/feedback/students?class_name={name}&subject_id={id}
Get all students in a class with their message counts

**Response:**
```json
[
  {
    "student_id": 1,
    "name": "Rohan Sharma",
    "email": "rohan.sharma.2q11@thapar.edu",
    "message_count": 5,
    "last_message_time": "2026-04-04 14:30"
  }
]
```

### GET /api/faculty/feedback?student_id={id}&subject_id={id}
Get full conversation thread with a student

**Response:**
```json
{
  "messages": [
    {
      "message": "I have a doubt about normalization",
      "timestamp": "2026-04-04 10:00:00",
      "sender_name": "Rohan Sharma",
      "sender_role": "student",
      "is_own_message": false
    },
    {
      "message": "Sure, what specific aspect would you like to discuss?",
      "timestamp": "2026-04-04 10:15:00",
      "sender_name": "Dr. Rajesh Kumar",
      "sender_role": "faculty",
      "is_own_message": true
    }
  ],
  "student": {
    "student_id": 1,
    "name": "Rohan Sharma",
    "class_name": "2Q11"
  }
}
```

### POST /api/faculty/feedback
Send a message to student

**Request Body:**
```json
{
  "student_id": 1,
  "subject_id": 1,
  "message": "Sure, what specific aspect would you like to discuss?"
}
```

**Response:**
```json
{
  "message": "Sure, what specific aspect would you like to discuss?",
  "timestamp": "2026-04-04 10:15:00",
  "sender_name": "Dr. Rajesh Kumar",
  "sender_role": "faculty",
  "is_own_message": true
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "message": "subject_id and message required"
}
```

### 401 Unauthorized
```json
{
  "message": "Token is missing"
}
```

### 403 Forbidden
```json
{
  "message": "Unauthorized access to this class"
}
```

### 404 Not Found
```json
{
  "message": "Student not found"
}
```

### 500 Internal Server Error
```json
{
  "message": "Server error occurred"
}
```

---

## Notes

1. All timestamps are in format: `YYYY-MM-DD HH:MM:SS`
2. Dates are in format: `YYYY-MM-DD`
3. Status values: `P` (Present), `A` (Absent)
4. Assessment types: `MST`, `EST`, `Assignment`, `Quiz`
5. Alert types: `Warning`, `Alert`, `Critical`
6. Roles: `student`, `faculty`

## Testing with cURL

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"rohan.sharma.2q11@thapar.edu","password":"pass123"}'
```

### Get Student Dashboard
```bash
curl -X GET http://localhost:5000/api/student/dashboard \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Send Feedback
```bash
curl -X POST http://localhost:5000/api/student/feedback \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"subject_id":1,"message":"I have a doubt"}'
```
