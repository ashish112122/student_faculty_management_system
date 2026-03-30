@echo off
echo ========================================
echo Student Management System - Quick Install
echo ========================================
echo.

echo Step 1: Installing Python packages...
cd backend
pip install Flask==2.3.0
pip install flask-cors==4.0.0
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0

echo.
echo Step 2: Installing Oracle DB driver...
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Install Oracle Database XE from: https://www.oracle.com/database/technologies/xe-downloads.html
echo 2. Run schema.sql and demo_data.sql in SQL Developer
echo 3. Update backend/config.py with your Oracle password
echo 4. Run: python app.py
echo.
pause
