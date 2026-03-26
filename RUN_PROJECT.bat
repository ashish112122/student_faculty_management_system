@echo off
title Student Management System

echo ========================================
echo Student Management System
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit
)

echo.
echo Checking Oracle Database...
sc query OracleServiceXE | find "RUNNING" >nul
if errorlevel 1 (
    echo WARNING: Oracle service is not running!
    echo Please start OracleServiceXE in services.msc
    pause
)

echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Servers Started!
echo ========================================
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Opening browser...
timeout /t 2 /nobreak >nul
start http://localhost:8000/login.html

echo.
echo Press any key to stop all servers...
pause >nul

taskkill /FI "WindowTitle eq Backend Server*" /T /F >nul 2>&1
taskkill /FI "WindowTitle eq Frontend Server*" /T /F >nul 2>&1

echo Servers stopped.
