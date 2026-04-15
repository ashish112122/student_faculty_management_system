@echo off
REM Start all required services for the Student Faculty Management System

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 STARTING STUDENT FACULTY MANAGEMENT SYSTEM             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Get the directory where this script is located
set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%venv
set BACKEND_DIR=%PROJECT_DIR%backend
set FRONTEND_DIR=%PROJECT_DIR%frontend

REM Check if venv exists
if not exist "%VENV_DIR%" (
    echo ❌ Virtual environment not found at %VENV_DIR%
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
echo ⏳ Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Check if backend is running
echo.
echo ⏳ Checking backend...
timeout /t 1 /nobreak > nul

REM Start backend in a new window
echo ⏳ Starting Backend (Flask server on port 5000)...
start "Backend Server" cmd /k "cd %BACKEND_DIR% && python app.py"
timeout /t 2 /nobreak > nul

REM Start frontend in a new window
echo ⏳ Starting Frontend (HTTP server on port 8000)...
start "Frontend Server" cmd /k "cd %PROJECT_DIR% && python start_frontend_server.py"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✓ ALL SERVERS STARTING                                   ║
echo ║                                                            ║
echo ║  Backend:  http://localhost:5000                          ║
echo ║  Frontend: http://localhost:8000                          ║
echo ║                                                            ║
echo ║  Login page will open automatically in your browser!      ║
echo ║  If not, go to: http://localhost:8000/login_test.html    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

timeout /t 5 /nobreak > nul
