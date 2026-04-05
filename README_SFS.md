# Student-Faculty Management System (SFS)

## Overview
A complete Student-Faculty Management System built with Flask backend, plain HTML5/CSS3/JS frontend, and Oracle Database integration.

## Features

### Student Dashboard
- View CGPA, semester, total credits
- Marks table with visualization (bar chart)
- Attendance tracking with progress bars
- Real-time alerts with unread highlighting
- Feedback messaging with faculty

### Faculty Dashboard
- Department overview
- Add/edit marks for students
- Mark attendance per class
- Marks distribution reports with charts
- Alert creation
- Feedback messaging with students

### Dynamic Updates
- Faculty marks → Auto-reflected in student dashboards
- Alerts → Real-time notifications
- Attendance → Auto-update progress bars
- CGPA → Auto-calculated based on marks

## Tech Stack

### Backend
- **Python 3.9+**
- **Flask 2.3.0**
- **Flask-CORS 3.1.1**
- **oracledb 1.3.0**
- **bcrypt 4.0.1** (Password hashing)
- **PyJWT** (JWT authentication)

### Frontend
- **HTML5** (Plain, no Bootstrap)
- **CSS3** (Custom styling)
- **JavaScript** (Vanilla)
- **Chart.js** (CDN for charts)

### Database
- **Oracle Database 11g/12c**
- **Tables**: Users, Students, Faculty, Departments, Subjects, Marks, Attendance, Alerts, Feedback

## Installation

### Prerequisites
- Python 3.9+
- Oracle Database (user: system, password: Vanshi@Oracle1)
- Git

### Setup
1. Clone and create feature branch:
```bash
git checkout -b feature/full_dynamic_sfs
git merge origin/ASHISH
git merge origin/VANSHIKA
git merge origin/GURLEEN
```

2. Install dependencies:
```bash
pip install Flask==2.3.0 oracledb==1.3.0 Flask-CORS==3.1.1 bcrypt==4.0.1 python-dotenv==1.0.0 PyJWT
```

3. Setup database:
```bash
python setup_db.py
python generate_students.py
python generate_marks_attendance.py
```

4. Run backend:
```bash
python app_complete.py
```

5. Open frontend:
```bash
Open templates/login.html in browser
```

## Database Configuration

```python
DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}
```

## API Routes

### Authentication
- `POST /register` - Student registration
- `POST /login` - Login (returns JWT token)
- `POST /logout` - Logout

### Student
- `GET /student/dashboard` - Student dashboard data
- `GET /student/marks` - All marks
- `GET /student/attendance` - Attendance records
- `GET /alerts/list/<student_id>` - View alerts

### Faculty
- `GET /faculty/dashboard` - Faculty dashboard data
- `POST /faculty/add_marks` - Add student marks
- `GET /faculty/marks_report/<subject_id>` - Marks distribution
- `POST /attendance/mark` - Mark attendance
- `GET /attendance/report` - Attendance report

### Feedback & Alerts
- `GET /feedback/list/<student_id>` - View feedback
- `POST /feedback/send` - Send feedback
- `GET /alerts/check` - Check new alerts

## Sample Data

- **150 Students** across 4 departments
- **4 Departments**: Computer Science, Electronics, Mechanical, Civil
- **3 Subjects** per department
- **2 Faculty** members

## File Structure

```
student_faculty_management_system/
├── app_complete.py              # Main Flask app
├── setup_db.py                  # Database initialization
├── generate_students.py         # Generate 150 students
├── generate_marks_attendance.py # Generate sample marks & attendance
├── templates/
│   ├── login.html              # Login page
│   ├── register.html           # Student registration
│   ├── student_dashboard.html  # Student dashboard
│   ├── faculty_dashboard.html  # Faculty dashboard
│   └── base.html               # Base template
├── static/
│   ├── app.js                  # Frontend logic
│   └── style.css               # Styling
├── sql/
│   ├── create_tables.sql       # Database schema
│   └── insert_sample_data.sql  # Initial data
└── backend/
    └── config.py               # Configuration
```

## JWT Authentication

All protected routes require:
```
Authorization: Bearer <token>
```

Token expires in 24 hours.

## Usage

### Student Login
1. Go to login.html
2. Email: `student2@univ.edu`, Password: `pass123`
3. Select "Student" role
4. View dashboard with marks, attendance, alerts

### Faculty Login
1. Email: `faculty1@univ.edu`, Password: `pass123`
2. Select "Faculty" role
3. Add marks or mark attendance
4. View reports and charts

## Features Implemented

✅ User Authentication (JWT)  
✅ Student Dashboard (CGPA, Marks, Attendance, Alerts)  
✅ Faculty Dashboard (Classes, Add Marks, Attendance)  
✅ Dynamic Charts (Chart.js)  
✅ Auto-update CGPA  
✅ Real-time Alerts  
✅ 150 Sample Students  
✅ Oracle Database Integration  
✅ Plain HTML/CSS/JS Frontend  
✅ Full FLASK Backend  

## Future Enhancements

- WebSocket for real-time updates
- Email notifications
- Mobile responsive design
- Advanced reporting
- Performance analytics

## Troubleshooting

### Database Connection Error
Check Oracle is running and credentials are correct in DB_CONFIG

### CORS Issues
Flask-CORS is configured to allow all origins

### Port 5000 in use
Change port in `app_complete.py`: `app.run(port=5001)`

## License
MIT

## Author
Student-Faculty Management Team
