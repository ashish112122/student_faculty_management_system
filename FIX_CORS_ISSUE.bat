@echo off
echo ========================================
echo CORS Connection Fix
echo ========================================
echo.

echo Step 1: Checking if backend is running...
echo.

curl -s http://localhost:5000/api/student/faculty >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend is NOT running on port 5000
    echo.
    echo SOLUTION: Start the backend server
    echo.
    echo Open a NEW terminal and run:
    echo   cd backend
    echo   python app.py
    echo.
    echo Then try again.
    pause
    exit /b 1
) else (
    echo ✓ Backend is running on port 5000
)

echo.
echo Step 2: Testing CORS headers...
echo.

curl -H "Origin: http://localhost:8000" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: Content-Type" -X OPTIONS http://localhost:5000/api/login -v 2>&1 | findstr "Access-Control"

if errorlevel 1 (
    echo.
    echo ❌ CORS headers not found
    echo.
    echo SOLUTION: Restart the backend
    echo   1. Stop backend (Ctrl+C)
    echo   2. cd backend
    echo   3. python app.py
    echo.
) else (
    echo.
    echo ✓ CORS headers are present
)

echo.
echo Step 3: Checking frontend...
echo.

curl -s http://localhost:8000/login.html >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend is NOT running on port 8000
    echo.
    echo SOLUTION: Start the frontend server
    echo.
    echo Open a NEW terminal and run:
    echo   cd frontend
    echo   python -m http.server 8000
    echo.
) else (
    echo ✓ Frontend is running on port 8000
)

echo.
echo ========================================
echo Diagnosis Complete
echo ========================================
echo.
echo If both servers are running but still getting errors:
echo 1. Clear browser cache (Ctrl+Shift+Delete)
echo 2. Try Incognito/Private mode
echo 3. Check browser console (F12) for exact error
echo.
pause
