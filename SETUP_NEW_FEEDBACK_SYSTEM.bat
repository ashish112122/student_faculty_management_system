@echo off
echo ========================================
echo   FEEDBACK THREADING SYSTEM SETUP
echo ========================================
echo.
echo This will:
echo   1. Migrate database to new threading system
echo   2. Update backend with new APIs
echo   3. Instructions for frontend update
echo.
echo ========================================
echo.

cd backend

echo Step 1: Running database migration...
echo.
python migrate_feedback_to_threads.py

echo.
echo ========================================
echo.
echo Step 2: Backend API Update
echo.
echo The new API endpoints are ready in:
echo   backend/update_app_with_feedback.py
echo.
echo You need to manually add these to backend/app.py
echo OR use the updated backend/app.py file
echo.
echo ========================================
echo.
echo Step 3: Frontend Update
echo.
echo New frontend files will be created:
echo   - frontend/feedback_threads.html
echo   - frontend/js/feedback_threads.js
echo   - frontend/css/feedback_threads.css
echo.
echo ========================================
echo.
echo Next Steps:
echo   1. Check if migration was successful
echo   2. Update backend/app.py with new routes
echo   3. Update frontend files
echo   4. Restart backend server
echo   5. Test the new system!
echo.
echo ========================================
echo.

pause
