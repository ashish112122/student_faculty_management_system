@echo off
echo ========================================
echo   OPENING LOGIN PAGE
echo ========================================
echo.
echo Opening: http://localhost:8000/login_test.html
echo.
echo Student Login:
echo   Email: rohan.sharma.2q34.3@thapar.edu
echo   Password: pass123
echo.
echo Faculty Login:
echo   Email: dr.rajesh@thaparfac.edu
echo   Password: pass123
echo.
echo ========================================

start http://localhost:8000/login_test.html

echo.
echo Login page opened in your browser!
echo.
pause
