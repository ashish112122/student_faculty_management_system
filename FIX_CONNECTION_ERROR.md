# 🚨 FIX: "Connection error. Please try again."

## ⚡ QUICK FIX (Do This First!)

### Step 1: Check if servers are running
```cmd
CHECK_SERVERS.bat
```

This will tell you exactly what's wrong.

### Step 2: If backend is not running
```cmd
cd backend
python app.py
```

**Keep this terminal open!**

### Step 3: If frontend is not running
Open a **NEW** terminal:
```cmd
cd frontend
python -m http.server 8000
```

**Keep this terminal open too!**

### Step 4: Try login again
Open browser: `http://localhost:8000/login.html`

---

## 🎯 What I Fixed

I've updated your `backend/app.py` with a more permissive CORS configuration that should work immediately.

**Changes made:**
- ✅ Simplified CORS configuration
- ✅ Added wildcard support for development
- ✅ Increased max_age for preflight caching
- ✅ Always send CORS headers

**You MUST restart the backend for this to work!**

---

## 🔄 Complete Restart (If Quick Fix Doesn't Work)

### 1. Stop Everything
- Close all terminals running Python
- Close browser

### 2. Start Backend
```cmd
cd backend
python app.py
```

**You should see:**
```
* Serving Flask app 'app'
* Debug mode: on
WARNING: This is a development server.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

**✅ If you see this, backend is running correctly!**

**❌ If you see errors:**
- Check if port 5000 is already in use
- Make sure oracledb is installed: `pip install oracledb`
- Check Oracle database is running

### 3. Start Frontend (New Terminal)
```cmd
cd frontend
python -m http.server 8000
```

**You should see:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/)
```

**✅ If you see this, frontend is running correctly!**

### 4. Test in Browser
1. Open: `http://localhost:8000/login.html`
2. Press **F12** to open Developer Tools
3. Click **Console** tab
4. Try to login with:
   - Email: `rohan.sharma@thapar.edu`
   - Password: `password123`

**✅ If login works:** You're done!

**❌ If you see errors in console:**
- Read the error message
- See troubleshooting section below

---

## 🔍 Detailed Troubleshooting

### Error 1: "Failed to fetch"

**In browser console:**
```
TypeError: Failed to fetch
```

**Cause:** Backend is not running

**Solution:**
```cmd
cd backend
python app.py
```

---

### Error 2: "CORS policy"

**In browser console:**
```
Access to fetch at 'http://localhost:5000/api/login' from origin 'http://localhost:8000' 
has been blocked by CORS policy
```

**Cause:** Backend was running before I updated the CORS config

**Solution:**
1. Stop backend (press Ctrl+C in backend terminal)
2. Start again: `python app.py`
3. Clear browser cache (Ctrl+Shift+Delete)
4. Try again

---

### Error 3: "ERR_CONNECTION_REFUSED"

**In browser console:**
```
GET http://localhost:5000/api/login net::ERR_CONNECTION_REFUSED
```

**Cause:** Backend is not running OR wrong port

**Solution:**
1. Check backend is running: `CHECK_SERVERS.bat`
2. If not running, start it: `cd backend && python app.py`
3. Verify it says "Running on http://127.0.0.1:5000"

---

### Error 4: "Invalid credentials"

**On login page:**
```
Invalid credentials
```

**Cause:** Database not set up OR wrong password

**Solution:**
1. Setup database: `SETUP_DATABASE_PYTHON.bat`
2. Use correct credentials:
   - Email: `rohan.sharma@thapar.edu`
   - Password: `password123`

---

## 🧪 Test CORS Directly

**Run this test:**
```cmd
cd backend
python test_cors.py
```

**Expected output:**
```
✓ Access-Control-Allow-Origin: http://localhost:8000
✓ Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
✓ Access-Control-Allow-Headers: Content-Type,Authorization
✅ CORS preflight is working!
✅ Login successful!
```

**If test fails:**
- Backend is not running
- Backend needs to be restarted
- Port 5000 is blocked by firewall

---

## 📋 Checklist

Go through this checklist:

- [ ] Backend terminal is open and showing "Running on http://127.0.0.1:5000"
- [ ] Frontend terminal is open and showing "Serving HTTP on :: port 8000"
- [ ] Browser is open to `http://localhost:8000/login.html` (not 5000!)
- [ ] Browser console (F12) shows no red errors
- [ ] Database is set up (ran SETUP_DATABASE_PYTHON.bat)
- [ ] Using correct login: rohan.sharma@thapar.edu / password123

---

## 🎯 Common Mistakes

### Mistake 1: Opening wrong URL
❌ `http://localhost:5000` (backend - shows "Not Found")
✅ `http://localhost:8000/login.html` (frontend - shows login page)

### Mistake 2: Closing terminals
❌ Closing the terminal after starting backend/frontend
✅ Keep both terminals open while using the app

### Mistake 3: Not restarting backend
❌ Updating code but not restarting backend
✅ Always restart backend after code changes (Ctrl+C then python app.py)

### Mistake 4: Wrong credentials
❌ Using random email/password
✅ Use: rohan.sharma@thapar.edu / password123

---

## 🚀 Easy Way (Automated)

**Just run this:**
```cmd
RUN_PROJECT.bat
```

This will:
1. ✅ Start backend automatically
2. ✅ Start frontend automatically
3. ✅ Open browser to correct URL
4. ✅ Show you both server windows

---

## 📞 Quick Commands Reference

```cmd
# Check what's running
CHECK_SERVERS.bat

# Start backend
cd backend
python app.py

# Start frontend (new terminal)
cd frontend
python -m http.server 8000

# Test CORS
cd backend
python test_cors.py

# Setup database
SETUP_DATABASE_PYTHON.bat

# Start everything (easy way)
RUN_PROJECT.bat
```

---

## ✅ Success Indicators

You'll know it's working when:

1. **Backend terminal shows:**
   ```
   * Running on http://127.0.0.1:5000
   ```

2. **Frontend terminal shows:**
   ```
   Serving HTTP on :: port 8000
   ```

3. **Browser shows:**
   - Login page loads
   - No errors in console (F12)
   - Login redirects to dashboard

4. **CHECK_SERVERS.bat shows:**
   ```
   ✓ Backend is running on port 5000
   ✓ Frontend is running on port 8000
   ✅ Both servers are running!
   ```

---

## 🎉 Summary

**Most likely cause:** Backend is not running

**Quick fix:**
1. Run `CHECK_SERVERS.bat` to see what's wrong
2. Start missing server(s)
3. Try login again

**If still not working:**
1. Stop everything
2. Run `RUN_PROJECT.bat`
3. Wait for browser to open
4. Try login

**The connection error should be fixed now!** 🚀
