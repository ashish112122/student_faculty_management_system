@echo off
echo ============================================================
echo TESTING LOGIN PAGE (No Redirect)
echo ============================================================
echo.

echo Opening test login page...
start "" "frontend\login_test.html"

echo.
echo This version will NOT redirect after login.
echo It will show a success message instead.
echo.
echo Test Credentials:
echo   Faculty: dr.rajesh@thaparfac.edu / pass123
echo   Student: rohan.sharma@thapar.edu / pass123
echo.
echo Backend should be running on http://localhost:5000
echo.
pause
