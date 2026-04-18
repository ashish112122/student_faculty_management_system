# How to Run and Login - Complete Guide

## 🚀 Opening Logic

### Backend Opening Logic

**Step 1: Start Backend Server**
```cmd
cd backend
python app.py
```

**What Happens:**
1. Flask server starts on `http://localhost:5000`
2. Connects to Oracle Database (system/Vanshi@Oracle1@localhost:1521/XE)
3. Initializes CORS for frontend communication
4. Loads all API endpoints:
   - `/api/login` - Authentication
   - `/api/student/*` - Student endpoints
   - `/api/faculty/*` - Faculty endpoints
5. Server ready message: "Backend running on http://localhost:5000"

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://localhost:5000
Press CTRL+C to quit
```

**Troubleshooting:**
- If port 5000 is busy: Change port in `app.py` line: `app.run(debug=True, port=5000)`
- If Oracle connection fails: Check credentials in `backend/config.py`
- If module not found: Run `pip install flask flask-cors cx_Oracle PyJWT`

---

### Frontend Opening Logic

**Step 1: Open Login Page**
```
Method 1: Double-click file
frontend/login_test.html

Method 2: Use Live Server (VS Code)
Right-click login_test.html → Open with Live Server

Method 3: Direct browser
Open browser → File → Open → Select frontend/login_test.html
```

**What Happens:**
1. Browser loads `login_test.html`
2. Page displays login form with:
   - Email input field
   - Password input field
   - Login button
3. JavaScript ready to handle form submission
4. Will send POST request to `http://localhost:5000/api/login`

**Expected URL:**
```
file:///C:/path/to/project/frontend/login_test.html
OR
http://localhost:5500/frontend/login_test.html (if using Live Server)
```

---

## 👤 Login Examples

### Student Login Example

**Credentials:**
```
Email: rahul.sharma@thapar.edu
Password: password123
```

**Step-by-Step:**
1. Open `frontend/login_test.html` in browser
2. Enter email: `rahul.sharma@thapar.edu`
3. Enter password: `password123`
4. Click "Login" button
5. Wait for "Login successful! Redirecting..." message
6. Automatically redirects to `student_portal.html`

**What Happens Behind the Scenes:**
```javascript
// 1. Form submission
POST http://localhost:5000/api/login
Body: {
  "email": "rahul.sharma@thapar.edu",
  "password": "password123"
}

// 2. Backend validates credentials
// 3. Backend returns response
Response: {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "student",
  "user_id": 1,
  "name": "Rahul Sharma"
}

// 4. Frontend stores in localStorage
localStorage.setItem('token', data.token);
localStorage.setItem('role', 'student');
localStorage.setItem('user_id', data.user_id);
localStorage.setItem('name', data.name);

// 5. Redirect to student portal
window.location.href = 'student_portal.html';
```

**After Login - Student Portal:**
- Dashboard shows: Name, Batch, Semester, CGPA
- Can access: Marks, Attendance, Alerts, Feedback
- Token persists on refresh
- Stays logged in until explicit logout

---

### Faculty Login Example

**Credentials:**
```
Email: amit.kumar@thaparfac.edu
Password: password123
```

**Step-by-Step:**
1. Open `frontend/login_test.html` in browser
2. Enter email: `amit.kumar@thaparfac.edu`
3. Enter password: `password123`
4. Click "Login" button
5. Wait for "Login successful! Redirecting..." message
6. Automatically redirects to `faculty_portal.html`

**What Happens Behind the Scenes:**
```javascript
// 1. Form submission
POST http://localhost:5000/api/login
Body: {
  "email": "amit.kumar@thaparfac.edu",
  "password": "password123"
}

// 2. Backend validates credentials
// 3. Backend returns response
Response: {
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "role": "faculty",
  "user_id": 1,
  "name": "Dr. Amit Kumar"
}

// 4. Frontend stores in localStorage
localStorage.setItem('token', data.token);
localStorage.setItem('role', 'faculty');
localStorage.setItem('user_id', data.user_id);
localStorage.setItem('name', data.name);

// 5. Redirect to faculty portal
window.location.href = 'faculty_portal.html';
```

**After Login - Faculty Portal:**
- Dashboard shows: Name, Department, Subject, Batches
- Can access: Marks Entry, Attendance, Feedback
- Token persists on refresh
- Stays logged in until explicit logout

---

## 📋 Complete Demo Credentials

### Students (Email format: @thapar.edu)

| Name | Email | Password | Batch | Roll No |
|------|-------|----------|-------|---------|
| Rahul Sharma | rahul.sharma@thapar.edu | password123 | BCA 3rd Year | 101 |
| Priya Singh | priya.singh@thapar.edu | password123 | BCA 3rd Year | 102 |
| Amit Patel | amit.patel@thapar.edu | password123 | BCA 3rd Year | 103 |
| Sneha Gupta | sneha.gupta@thapar.edu | password123 | BCA 3rd Year | 104 |
| Rohan Verma | rohan.verma@thapar.edu | password123 | BCA 3rd Year | 105 |

### Faculty (Email format: @thaparfac.edu)

| Name | Email | Password | Department | Subject |
|------|-------|----------|------------|---------|
| Dr. Amit Kumar | amit.kumar@thaparfac.edu | password123 | Computer Science | Database Management |
| Dr. Priya Sharma | priya.sharma@thaparfac.edu | password123 | Computer Science | Data Structures |
| Dr. Rajesh Singh | rajesh.singh@thaparfac.edu | password123 | Computer Science | Operating Systems |
| Dr. Neha Gupta | neha.gupta@thaparfac.edu | password123 | Computer Science | Computer Networks |
| Dr. Vikram Patel | vikram.patel@thaparfac.edu | password123 | Computer Science | Software Engineering |

---

## 🔄 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    START APPLICATION                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Start Backend                                      │
│  Command: cd backend && python app.py                       │
│  Result: Server running on http://localhost:5000            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Open Frontend                                      │
│  File: frontend/login_test.html                             │
│  Result: Login page displayed in browser                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Enter Credentials                                  │
│  Student: rahul.sharma@thapar.edu / password123             │
│  Faculty: amit.kumar@thaparfac.edu / password123            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Click Login Button                                 │
│  Action: POST /api/login                                    │
│  Backend validates credentials                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────┴───────┐
                    │               │
            ┌───────▼─────┐   ┌────▼──────┐
            │   Student   │   │  Faculty  │
            │   Portal    │   │  Portal   │
            └─────────────┘   └───────────┘
                    │               │
            ┌───────▼─────┐   ┌────▼──────┐
            │ Dashboard   │   │ Dashboard │
            │ Marks       │   │ Marks     │
            │ Attendance  │   │ Attendance│
            │ Alerts      │   │ Feedback  │
            │ Feedback    │   │           │
            └─────────────┘   └───────────┘
```

---

## 🛠️ Quick Start Commands

### Windows (CMD)

```cmd
REM Terminal 1 - Backend
cd backend
python app.py

REM Terminal 2 - Frontend (if using http-server)
cd frontend
npx http-server -p 8080

REM Then open browser:
REM http://localhost:8080/login_test.html
```

### Alternative - Direct File Opening

```cmd
REM Start backend only
cd backend
python app.py

REM Then double-click:
REM frontend/login_test.html
```

---

## 🔍 Verification Steps

### 1. Check Backend is Running
```cmd
curl http://localhost:5000/api/login
```
Expected: Method Not Allowed (405) - means server is running

### 2. Check Frontend Loads
- Open browser console (F12)
- Should see no errors
- Login form should be visible

### 3. Test Login
- Enter credentials
- Check browser console for:
  - "Login successful! Redirecting..."
  - No CORS errors
  - No 404 errors

### 4. Verify Token Storage
- After login, open browser console
- Type: `localStorage.getItem('token')`
- Should return a JWT token string

---

## ❌ Common Issues and Solutions

### Issue 1: CORS Error
```
Error: Access to fetch at 'http://localhost:5000/api/login' from origin 'null' has been blocked by CORS policy
```
**Solution:** Backend is not running. Start with `python app.py`

### Issue 2: Connection Refused
```
Error: Failed to fetch
```
**Solution:** Backend not started or wrong port. Check `http://localhost:5000`

### Issue 3: Invalid Credentials
```
Error: Invalid email or password
```
**Solution:** Use exact credentials from demo data (case-sensitive)

### Issue 4: Page Not Redirecting
```
Login successful but stays on login page
```
**Solution:** Check browser console for JavaScript errors

### Issue 5: Token Not Persisting
```
Logged out after refresh
```
**Solution:** Check if localStorage is enabled in browser settings

---

## 📝 Testing Checklist

- [ ] Backend starts without errors
- [ ] Login page loads in browser
- [ ] Student login works (rahul.sharma@thapar.edu)
- [ ] Faculty login works (amit.kumar@thaparfac.edu)
- [ ] Student portal displays dashboard
- [ ] Faculty portal displays dashboard
- [ ] Refresh keeps user logged in
- [ ] Logout button works
- [ ] Can navigate between sections
- [ ] Data loads correctly

---

## 🎯 Success Indicators

**Backend Running Successfully:**
```
✓ No error messages in terminal
✓ Shows "Running on http://localhost:5000"
✓ Can access http://localhost:5000 in browser
```

**Frontend Working Successfully:**
```
✓ Login page displays correctly
✓ No console errors (F12)
✓ Login button is clickable
✓ Success message appears after login
```

**Login Working Successfully:**
```
✓ Redirects to correct portal (student/faculty)
✓ Dashboard shows user name
✓ All sections are accessible
✓ Token stored in localStorage
✓ Refresh doesn't log out user
```

---

## 🔐 Security Notes

**For Development:**
- Passwords are plain text in demo data
- JWT secret is hardcoded
- CORS allows all origins
- Debug mode is enabled

**For Production:**
- Hash all passwords with bcrypt
- Use environment variables for secrets
- Restrict CORS to specific domains
- Disable debug mode
- Use HTTPS
- Implement rate limiting

---

## 📞 Need Help?

If you encounter issues:

1. Check backend terminal for errors
2. Check browser console (F12) for errors
3. Verify Oracle database is running
4. Confirm credentials match demo data
5. Try different browser
6. Clear localStorage and try again

**Quick Reset:**
```javascript
// In browser console
localStorage.clear();
sessionStorage.clear();
location.reload();
```

---

## ✅ Ready to Start!

1. Open Terminal → `cd backend` → `python app.py`
2. Open Browser → `frontend/login_test.html`
3. Login with demo credentials
4. Enjoy the portal!

**Student Test:** rahul.sharma@thapar.edu / password123
**Faculty Test:** amit.kumar@thaparfac.edu / password123
