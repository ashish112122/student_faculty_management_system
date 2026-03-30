@echo off
cls
echo ========================================
echo Simple Database Setup
echo ========================================
echo.
echo This will:
echo 1. Drop all existing tables
echo 2. Create fresh tables
echo 3. Insert demo data
echo.
echo Make sure Oracle service is running!
echo.
pause

cd backend
python setup_simple.py
cd ..

echo.
echo ========================================
echo.
pause
