@echo off
echo ============================================================
echo STUDENT-FACULTY PORTAL - SETUP
echo ============================================================
echo.

cd backend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install flask flask-cors oracledb pyjwt

echo.
echo ============================================================
echo RUNNING SETUP SCRIPT
echo ============================================================
echo.

python setup.py

echo.
echo ============================================================
echo SETUP COMPLETE!
echo ============================================================
echo.
echo To start the backend server, run:
echo   START_SERVER.bat
echo.
pause
