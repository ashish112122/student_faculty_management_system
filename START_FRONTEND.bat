@echo off
echo ============================================================
echo STARTING FRONTEND SERVER
echo ============================================================
echo.

cd frontend
echo Starting HTTP server on port 8000...
echo.
echo Open your browser and go to:
echo http://localhost:8000/login_no_logo.html
echo.
echo Press Ctrl+C to stop the server
echo.

python -m http.server 8000
