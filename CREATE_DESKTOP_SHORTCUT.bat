@echo off
echo ========================================
echo   CREATING DESKTOP SHORTCUT
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Start Student System.lnk

echo Creating shortcut on Desktop...
echo.

powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%SCRIPT_DIR%START_ALL.bat'; $Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $Shortcut.Description = 'Start Student Faculty Management System'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo ========================================
    echo   SUCCESS!
    echo ========================================
    echo.
    echo Shortcut created on Desktop:
    echo   "Start Student System"
    echo.
    echo You can now double-click this shortcut
    echo to start the entire system!
    echo.
) else (
    echo ERROR: Failed to create shortcut
    echo.
)

pause
