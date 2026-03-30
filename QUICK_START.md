# Quick Start Guide

## First Time Setup (Do Once)

### 1. Install Oracle Database Package
```cmd
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

### 2. Install Other Requirements
```cmd
cd backend
pip install -r requirements.txt
```

### 3. Setup Database Tables
```cmd
SETUP_DATABASE_PYTHON.bat
```

## Running the Application (Every Time)

### Option 1: Automatic (Recommended)
```cmd
START_SERVERS.bat
```

### Option 2: Manual
Open two separate terminals:

Terminal 1 - Backend:
```cmd
cd backend
python app.py
```

Terminal 2 - Frontend:
```cmd
cd frontend
python -m http.server 8000
```

Then open: http://localhost:8000/login.html

## Demo Credentials

### Students
- Email: rohan.sharma@thapar.edu
- Password: password123

### Faculty
- Email: rohan.sharma@thaparfac.edu
- Password: password123

## Troubleshooting

### Login button does nothing?
1. Open browser console (F12)
2. Check for error messages
3. Run: `CHECK_SERVERS.bat` to verify both servers are running
4. Make sure database is setup (run SETUP_DATABASE_PYTHON.bat)

### Connection Error?
- Backend not running → Start backend server
- Frontend not running → Start frontend server
- Database not setup → Run SETUP_DATABASE_PYTHON.bat

### Still not working?
1. Clear browser cache (Ctrl+Shift+Delete)
2. Try Incognito mode (Ctrl+Shift+N)
3. Check if Oracle database is running
4. Verify credentials in backend/config.py
