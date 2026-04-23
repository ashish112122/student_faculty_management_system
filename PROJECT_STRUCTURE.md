# PROJECT STRUCTURE

## Clean Project Organization

### Root Directory
```
project/
├── backend/              # Backend application
├── frontend/             # Frontend HTML pages
├── static/               # Static assets
├── templates/            # Templates
├── uploads/              # File uploads
├── README.md             # Project documentation
├── WORKING_LINKS.md      # Working credentials and links
└── DATABASE_CREDENTIALS_REFERENCE.md  # Database info
```

### Backend Structure
```
backend/
├── archive/              # Old files (69 files archived)
├── tests/                # Test files (14 files)
├── database/
│   ├── schema.sql                      # Main database schema
│   └── schema_feedback_threads.sql     # Feedback system schema
├── app.py                              # Main Flask application
├── config.py                           # Database configuration
├── requirements.txt                    # Python dependencies
├── cleanup_database.py                 # Database cleanup utility
├── setup_complete_system.py            # Database setup script
├── verify_credentials.py               # Credential verification
└── test_system_after_cleanup.py        # System testing
```

### Frontend Structure
```
frontend/
├── archive/              # Old files (17 files archived)
├── assets/               # Images and assets
├── css/                  # Stylesheets
├── js/                   # JavaScript files
├── templates/            # HTML templates
├── login_test.html                     # Main login page
├── student_portal.html                 # Student interface
├── faculty_portal.html                 # Faculty interface
└── test_backend_connection.html        # Connection test
```

## Cleanup Summary

### Files Organized:
- 14 test files → backend/tests/
- 38 old backend files → backend/archive/
- 17 old frontend files → frontend/archive/

### Files Deleted:
- 30 unnecessary root Python files
- 34 old batch files
- 3 old HTML files
- 2 git error files
- 121 documentation .md files
- 3 cleanup script files

**Total: 208 files cleaned up**

## Essential Files Kept

### Backend (8 files):
1. app.py - Main application
2. config.py - Database configuration
3. requirements.txt - Dependencies
4. cleanup_database.py - Cleanup utility
5. setup_complete_system.py - Database setup
6. verify_credentials.py - Verification
7. test_system_after_cleanup.py - Testing
8. .env.example - Environment template

### Database (2 files):
1. schema.sql - Main schema
2. schema_feedback_threads.sql - Feedback schema

### Frontend (4 files):
1. login_test.html - Login page
2. student_portal.html - Student interface
3. faculty_portal.html - Faculty interface
4. test_backend_connection.html - Connection test

### Documentation (3 files):
1. README.md - Project documentation
2. WORKING_LINKS.md - Credentials and links
3. DATABASE_CREDENTIALS_REFERENCE.md - Database info

## How to Use

### Start Backend:
```bash
cd backend
python app.py
```

### Open Frontend:
```
frontend/login_test.html
```

### Login Credentials:
**Student:** rohan.sharma.2q34.3@thapar.edu / pass123
**Faculty:** dr.rajesh@thaparfac.edu / pass123

## Archive Folders

You can safely delete these folders after verifying everything works:
- backend/archive/ (38 files)
- backend/tests/ (14 files)
- frontend/archive/ (17 files)

## Status

✓ Project cleaned and organized
✓ All essential files present
✓ Database connection verified
✓ Credentials working
✓ System ready to use
