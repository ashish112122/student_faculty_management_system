@echo off
echo ========================================
echo   VERIFYING ALL FIXES
echo ========================================
echo.

cd backend
python verify_fixes.py

echo.
pause
