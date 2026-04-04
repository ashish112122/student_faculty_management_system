# Student-Faculty Management Portal

A comprehensive class-based student-faculty management system with real-time feedback, marks management, attendance tracking, and automatic alerts.

## 🚀 Quick Start

### 1. Configure Database
Edit `backend/config.py`:
```python
DB_USER = 'system'
DB_PASSWORD = 'your_password'
DB_DSN = 'localhost:1521/XE'
```

### 2. Setup Database
```bash
# Windows
SETUP.bat

# Linux/Mac
cd backend
python setup.py
```

### 3. Start Server
```bash
# Windows
START_SERVER.bat

# Linux/Mac
cd backend
python app.py
```

Server runs at: `http://localhost:5000`

## 📚 Features

- **5 Classes**: 2Q11, 2Q12, 2Q13, 2Q14, 2Q15 with 30 students each
- **Real-Time Feedback**: Full-duplex chat between students and faculty
- **Class-Based Marks**: Add/update marks with detailed reports
- **Attendance Tracking**: From Jan 1, 2026 to present with automatic alerts
- **Secure Access**: JWT authentication with role-based permissions

## 🎯 Test Credentials

### Faculty
```
Email: dr.rajesh@thaparfac.edu
Password: pass123
```

### Student
```
Email: rohan.sharma@thapar.edu
Password: pass123
```

See `CREDENTIALS.md` for complete list.

## 📖 Documentation

- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation
- **[CREDENTIALS.md](CREDENTIALS.md)** - All test credentials
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - Frontend development guide

## 🏗️ Project Structure

```
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Database configuration
│   ├── setup.py               # Database setup script
│   ├── generate_data.py       # Demo data generator
│   └── database/
│       └── schema.sql         # Database schema
├── frontend/
│   ├── templates/             # HTML pages
│   ├── js/                    # JavaScript files
│   └── css/                   # Stylesheets
├── SETUP.bat                  # Windows setup script
├── START_SERVER.bat           # Windows server start script
└── README.md                  # This file
```

## 🔧 Requirements

- Python 3.8+
- Oracle Database 11g+
- Flask, Flask-CORS, oracledb, PyJWT

## 📊 Database

After setup, you'll have:
- 10 Faculty members
- 150 Students (30 per class)
- 5 Subjects
- Complete marks and attendance data
- Automatic alerts for low attendance

## 🐛 Troubleshooting

### Database Connection Error
- Verify Oracle service is running
- Check credentials in `backend/config.py`
- Test connection: `python backend/test_connection.py`

### Login Issues
- Ensure database is set up: `python backend/check_setup.py`
- Verify credentials in `CREDENTIALS.md`

## 📞 Support

For issues:
1. Check documentation files
2. Review error messages in backend console
3. Verify database connectivity

---

**Version**: 2.0  
**Status**: Production Ready  
**License**: Educational Use
