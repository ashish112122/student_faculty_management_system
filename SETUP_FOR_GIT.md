# Git Setup Guide - Protecting Sensitive Files

## Files with Credentials (DO NOT COMMIT)

The following files contain sensitive credentials and are excluded from Git:

### Configuration Files
- `backend/config.py` - Contains Oracle password
- `backend/.env` - Environment variables with credentials
- `backend/setup_simple.py` - Database setup with credentials
- `backend/test_connection.py` - Connection test with credentials

### Batch Scripts
- `SETUP_SIMPLE.bat` - Contains database credentials
- `CHECK_DATABASE.bat` - Contains database credentials
- `TEST_LOGIN_ERROR.bat` - Contains database credentials

### Documentation Files
- All `*_SUMMARY.md` files
- All `*_COMPLETE.md` files
- All `DEBUG_*.md` files
- All `FIX_*.md` files

## Template Files (SAFE TO COMMIT)

Use these template files instead:

1. `backend/config.template.py` → Copy to `backend/config.py`
2. `backend/.env.example` → Copy to `backend/.env`
3. `backend/setup_simple.template.py` → Copy to `backend/setup_simple.py`

## Setup Instructions for Team Members

### 1. Clone Repository
```bash
git clone <repository-url>
cd student_faculty_management_system
```

### 2. Create Configuration Files
```bash
# Copy template files
cp backend/config.template.py backend/config.py
cp backend/.env.example backend/.env
cp backend/setup_simple.template.py backend/setup_simple.py
```

### 3. Update Credentials
Edit the following files with your Oracle credentials:

**backend/config.py:**
```python
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD_HERE'
```

**backend/setup_simple.py:**
```python
DB_PASSWORD = 'YOUR_ORACLE_PASSWORD_HERE'
```

### 4. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
pip install oracledb
```

### 5. Setup Database
```bash
python setup_simple.py
```

### 6. Run Application
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
python -m http.server 8000
```

## Before Committing

Always check what you're committing:

```bash
# Check status
git status

# Check diff
git diff

# Make sure no credentials are visible
git diff | grep -i password
```

## .gitignore is Already Configured

The `.gitignore` file already excludes:
- Configuration files with credentials
- Database files
- Batch scripts with credentials
- Local wheel files
- Temporary documentation files

## Safe to Commit

These files are safe to commit:
- All HTML files
- All CSS files
- All JavaScript files (no credentials)
- `backend/app.py` (uses config.py for credentials)
- `backend/requirements.txt`
- `backend/database/schema.sql`
- `backend/database/demo_data.sql`
- Template files (*.template.py, .env.example)
- README.md
- FIXES_APPLIED.md
- This file (SETUP_FOR_GIT.md)
