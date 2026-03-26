# Project Structure

```
student-management-system/
│
├── frontend/
│   ├── login.html                 # Login page
│   ├── dashboard.html             # Student dashboard
│   ├── marks.html                 # Marks module
│   ├── attendance.html            # Attendance module
│   ├── alerts.html                # Alerts module
│   ├── feedback.html              # Feedback module
│   ├── faculty-dashboard.html     # Faculty placeholder
│   │
│   ├── css/
│   │   ├── login.css
│   │   ├── dashboard.css
│   │   ├── marks.css
│   │   ├── attendance.css
│   │   ├── alerts.css
│   │   └── feedback.css
│   │
│   ├── js/
│   │   ├── login.js
│   │   ├── dashboard.js
│   │   ├── marks.js
│   │   ├── attendance.js
│   │   ├── alerts.js
│   │   └── feedback.js
│   │
│   └── assets/
│       └── university-logo.png    # Add your logo here
│
├── backend/
│   ├── app.py                     # Main Flask application
│   ├── config.py                  # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   │
│   ├── database/
│   │   ├── schema.sql             # Database schema
│   │   └── demo_data.sql          # Demo data (40 students, 10 faculty)
│   │
│   └── utils/
│       ├── alert_checker.py       # Attendance alert checker
│       └── email_service.py       # Email notification service
│
├── README.md                      # Setup and usage guide
├── TABLE_OWNERSHIP.md             # Database table ownership
├── INTEGRATION_GUIDE.md           # Team integration guide
└── .gitignore                     # Git ignore file
```

## Key Features

### Member 1 Deliverables
✓ Login system with role detection
✓ Student dashboard with sidebar
✓ Marks module with Chart.js graphs
✓ Attendance module with progress bars
✓ Alerts system with email notifications
✓ Feedback module with threaded conversations
✓ Complete database schema
✓ 40 student demo data
✓ 10 faculty demo data
✓ RESTful API with JWT authentication

### Architecture Highlights
- Modular design for easy team integration
- No file conflicts between members
- Shared database tables with clear ownership
- Snake_case naming convention
- Production-ready code structure
