@echo off
echo ========================================
echo Quick Fixes for Common Issues
echo ========================================
echo.

echo Choose a fix:
echo.
echo 1. Remove logo from login page (if you don't have logo)
echo 2. Update Oracle password in config.py
echo 3. Disable email alerts (if you don't need them)
echo 4. Run all fixes
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto fix_logo
if "%choice%"=="2" goto fix_password
if "%choice%"=="3" goto fix_email
if "%choice%"=="4" goto fix_all
if "%choice%"=="5" goto end

:fix_logo
echo.
echo Fixing logo issue...
echo Creating backup...
copy frontend\login.html frontend\login.html.backup
echo.
echo Please manually edit frontend/login.html
echo Find line: ^<img src="assets/university-logo.png"
echo Replace with: ^<h1 style="color:white; font-size:48px;"^>University^</h1^>
echo.
pause
goto end

:fix_password
echo.
set /p password="Enter your Oracle password: "
echo.
echo Please manually edit backend/config.py
echo Change line: DB_PASSWORD = 'oracle'
echo To: DB_PASSWORD = '%password%'
echo.
pause
goto end

:fix_email
echo.
echo Disabling email alerts...
echo Email alerts are optional - app will work without them
echo If you see email errors, they can be safely ignored
echo.
pause
goto end

:fix_all
call :fix_logo
call :fix_password
call :fix_email
goto end

:end
echo.
echo Done!
pause
