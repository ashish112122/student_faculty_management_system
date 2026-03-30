@echo off
echo ========================================
echo Installing Oracle DB Python Package
echo ========================================
echo.

echo Installing from your downloaded wheel file...
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl

echo.
echo Verifying installation...
python -c "import oracledb; print('✓ oracledb version:', oracledb.__version__)"

if errorlevel 1 (
    echo.
    echo ✗ Installation failed!
    echo.
    echo Try these solutions:
    echo 1. Make sure the file exists at: C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
    echo 2. Check you're using Python 3.11
    echo 3. Try: pip install oracledb
    echo.
) else (
    echo.
    echo ========================================
    echo ✓ Oracle DB package installed successfully!
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Install Oracle Database XE
    echo 2. Run: cd backend
    echo 3. Run: python test_connection.py
    echo.
)

pause
