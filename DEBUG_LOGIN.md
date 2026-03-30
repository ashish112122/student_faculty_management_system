# 🔧 Debug Login Issue

## Problem: Login button does nothing

This usually means JavaScript is not running or there's an error.

---

## 🎯 Quick Diagnosis

### Step 1: Open Test Page
```
http://localhost:8000/test_login.html
```

This page will:
- ✅ Show all console logs
- ✅ Test the login directly
- ✅ Show exact error messages
- ✅ Tell you what's wrong

### Step 2: Check Browser Console
1. Open login page: `http://localhost:8000/login.html`
2. Press **F12** to open Developer Tools
3. Click **Console** tab
4. Refresh the page
5. Look for errors (red text)

**What you should see:**
```
(no errors)
```

**If you see errors:**
- Red text = JavaScript error
- Read the error message
- See solutions below

### Step 3: Try Login
1. Enter email: `rohan.sharma@thapar.edu`
2. Enter password: `password123`
3. Click Login
4. Watch the Console tab

**What you should see:**
```
Login form submitted
Email: rohan.sharma@thapar.edu
Attempting login...
Sending request to backend...
Response status: 200
Login successful!
Redirecting to dashboard...
```

---

## 🔍 Common Issues

### Issue 1: JavaScript Not Loading

**Symptoms:**
- Nothing happens when clicking Login
- No console logs at all
- No errors in console

**Check:**
1. Open `http://localhost:8000/login.html`
2. Press F12 → Console
3. Type: `document.getElementById('loginForm')`
4. Press Enter

**If you see:** `null`
**Cause:** Form not found
**Solution:** Check HTML file has `id="loginForm"`

**If you see:** `<form id="loginForm">...</form>`
**Cause:** JavaScript file not loaded
**Solution:** Check `<script src="js/login.js"></script>` in HTML

### Issue 2: CORS Error

**Symptoms:**
- Console shows: "blocked by CORS policy"
- Login button does nothing
- Red error in console

**Solution:**
1. Stop backend (Ctrl+C)
2. Restart: `cd backend && python app.py`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try again

### Issue 3: Backend Not Running

**Symptoms:**
- Console shows: "Failed to fetch"
- Console shows: "ERR_CONNECTION_REFUSED"
- Error message: "Connection error"

**Solution:**
```cmd
cd backend
python app.py
```

Keep terminal open!

### Issue 4: Wrong URL

**Symptoms:**
- Page loads but looks broken
- Images don't load
- JavaScript doesn't work

**Check URL:**
❌ `file:///C:/Users/.../login.html` (Wrong - opened as file)
✅ `http://localhost:8000/login.html` (Correct - served by Python)

**Solution:**
```cmd
cd frontend
python -m http.server 8000
```

Then open: `http://localhost:8000/login.html`

### Issue 5: Database Not Setup

**Symptoms:**
- Login works but shows "Invalid credentials"
- Backend shows database errors

**Solution:**
```cmd
SETUP_DATABASE_PYTHON.bat
```

---

## 🧪 Test Files Created

### 1. Test Login Page
```
http://localhost:8000/test_login.html
```

Features:
- ✅ Pre-filled credentials
- ✅ Shows all console logs
- ✅ Shows exact errors
- ✅ Tests backend connectivity
- ✅ Shows response data

### 2. Updated login.js
- ✅ Added detailed console logs
- ✅ Better error messages
- ✅ Shows what's happening at each step

---

## 📋 Debugging Checklist

Go through this in order:

1. **Check backend is running**
   ```cmd
   CHECK_SERVERS.bat
   ```
   Should show: ✓ Backend is running on port 5000

2. **Check frontend is running**
   Should show: ✓ Frontend is running on port 8000

3. **Open test page**
   ```
   http://localhost:8000/test_login.html
   ```
   Click "Test Login" button

4. **Check console output**
   Should show: ✅ Login successful!

5. **If test page works, try real login page**
   ```
   http://localhost:8000/login.html
   ```

6. **Open browser console (F12)**
   Watch for errors when clicking Login

---

## 🔧 Manual Test

If nothing works, test manually:

### 1. Open Browser Console
Press F12 → Console tab

### 2. Paste this code:
```javascript
fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'rohan.sharma@thapar.edu',
        password: 'password123'
    })
})
.then(r => r.json())
.then(d => console.log('Success:', d))
.catch(e => console.error('Error:', e));
```

### 3. Press Enter

**Expected result:**
```javascript
Success: {
  token: "eyJ0eXAiOiJKV1QiLCJhbGc...",
  user_id: 11,
  role: "student",
  name: "Rohan Sharma"
}
```

**If this works:**
- ✅ Backend is working
- ✅ Database is setup
- ✅ CORS is working
- ❌ Problem is in login.js

**If this fails:**
- ❌ Backend issue
- See error message for details

---

## 🎯 Most Likely Causes

1. **Backend not running** (70%)
   - Solution: `cd backend && python app.py`

2. **Wrong URL** (15%)
   - Solution: Use `http://localhost:8000/login.html`

3. **JavaScript error** (10%)
   - Solution: Check console for red errors

4. **CORS issue** (5%)
   - Solution: Restart backend

---

## 📞 Quick Commands

```cmd
# Check servers
CHECK_SERVERS.bat

# Start backend
cd backend
python app.py

# Start frontend
cd frontend
python -m http.server 8000

# Open test page
start http://localhost:8000/test_login.html

# Open login page
start http://localhost:8000/login.html
```

---

## ✅ Success Indicators

Login is working when:

1. **Console shows:**
   ```
   Login form submitted
   Email: rohan.sharma@thapar.edu
   Attempting login...
   Response status: 200
   Login successful!
   ```

2. **Page redirects to dashboard**

3. **No errors in console**

4. **Test page shows ✅ Login Successful!**

---

**Try the test page first: `http://localhost:8000/test_login.html`**

**It will tell you exactly what's wrong!** 🚀
