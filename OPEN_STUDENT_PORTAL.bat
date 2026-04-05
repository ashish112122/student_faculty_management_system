@echo off
echo ========================================
echo   STUDENT PORTAL
echo ========================================
echo.
echo Opening student login page...
echo.
echo Test Credentials:
echo Email: rohan.das.2q15.0@thapar.edu
echo Password: pass123
echo.
start http://localhost:5000
start frontend/login_test.html
echo.
echo Portal opened in browser!
pause
