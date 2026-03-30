@echo off
cls
echo ========================================
echo Testing Login API - Finding 500 Error
echo ========================================
echo.

cd backend
python test_login_api.py

echo.
echo ========================================
echo.
echo If you see errors above, that's why login fails!
echo.
echo Common fixes:
echo 1. Database not running - Start Oracle service
echo 2. Tables not created - Run SETUP_DATABASE_PYTHON.bat
echo 3. Wrong password - Check backend/config.py
echo.
pause
