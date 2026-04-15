@echo off
REM Start only the frontend server

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🌐 STARTING FRONTEND SERVER                               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Get the directory where this script is located
set PROJECT_DIR=%~dp0
set VENV_DIR=%PROJECT_DIR%venv

REM Check if venv exists
if not exist "%VENV_DIR%" (
    echo ❌ Virtual environment not found
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Start frontend
cd %PROJECT_DIR%
python start_frontend_server.py

REM If we get here, the server was stopped
pause
