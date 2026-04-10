@echo off
echo ========================================
echo   STARTING FRONTEND SERVER
echo ========================================
echo.

cd frontend

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting frontend server on http://localhost:8000
echo.
echo Frontend will be available at:
echo   http://localhost:8000/login_test.html
echo.
echo This window must stay open.
echo Press Ctrl+C to stop the frontend server.
echo.
echo ========================================
echo.

python -m http.server 8000

pause
