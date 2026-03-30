# 🔧 Troubleshoot Connection Error

## "Connection error. Please try again."

This error means the frontend cannot reach the backend. Let's fix it step by step.

---

## 🚨 Quick Fix (Most Common Issue)

### The backend is probably not running!

**Check if backend is running:**
1. Look for a terminal window with `python app.py` running
2. It should show: `* Running on http://127.0.0.1:5000`

**If you don't see this, start the backend:**
```cmd
cd backend
python app.py
```

**Keep this terminal open!** Don't close it.

---

## ✅ Step-by-Step Diagnosis

### Step 1: Check Backend is Running

**Open Command Prompt and run:**
```cmd
curl http://localhost:5000/api/student/faculty
```

**Expected result:**
```json
{"message": "Token is missing"}
```

**If you see this:** ✅ Backend is running!

**If you see "Connection refused" or "Failed to connect":** ❌ Backend is NOT running

**Solution:**
```cmd
cd backend
python app.py
```

---

### Step 2: Check Frontend is Running

**Open browser to:**
```
http://localhost:8000/login.html
```

**If page loads:** ✅ Frontend is running!

**If "This site can't be reached":** ❌ Frontend is NOT running

**Solution:**
```cmd
cd frontend
python -m http.server 8000
```

---

### Step 3: Check Browser Console

1. Open the login page: `http://localhost:8000/login.html`
2. Press **F12** to open Developer Tools
3. Click **Console** tab
4. Try to login
5. Look for errors

**Common errors and solutions:**

#### Error: "Failed to fetch"
```
TypeError: Failed to fetch
```
**Cause:** Backend is not running
**Solution:** Start backend with `python app.py`

#### Error: "CORS policy"
```
Access to fetch at 'http://localhost:5000/api/login' from origin 'http://localhost:8000' 
has been blocked by CORS policy
```
**Cause:** Backend needs to be restarted
**Solution:** 
1. Stop backend (Ctrl+C)
2. Start again: `python app.py`

#### Error: "net::ERR_CONNECTION_REFUSED"
```
GET http://localhost:5000/api/login net::ERR_CONNECTION_REFUSED
```
**Cause:** Backend is not running
**Solution:** Start backend with `python app.py`

---

### Step 4: Verify CORS Configuration

**Run the test script:**
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
```

**If CORS test fails:**
1. Stop backend (Ctrl+C)
2. Restart: `python app.py`
3. Test again

---

## 🎯 Complete Restart Procedure

If nothing works, do a complete restart:

### 1. Stop Everything
- Close all terminal windows
- Close browser

### 2. Start Backend
```cmd
cd backend
python app.py
```

**Wait for:**
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Keep this terminal open!**

### 3. Start Frontend (New Terminal)
```cmd
cd frontend
python -m http.server 8000
```

**Wait for:**
```
Serving HTTP on :: port 8000
```

**Keep this terminal open too!**

### 4. Clear Browser Cache
- Press **Ctrl+Shift+Delete**
- Select "Cached images and files"
- Click "Clear data"

### 5. Open in Incognito Mode
- Press **Ctrl+Shift+N** (Chrome) or **Ctrl+Shift+P** (Firefox)
- Go to: `http://localhost:8000/login.html`
- Try login

---

## 🔍 Automated Diagnosis

**Run this to check everything:**
```cmd
FIX_CORS_ISSUE.bat
```

This will:
- ✅ Check if backend is running
- ✅ Check if frontend is running
- ✅ Test CORS headers
- ✅ Show you what's wrong

---

## 📊 Port Checklist

Make sure these ports are correct:

| Service | Port | URL | Status |
|---------|------|-----|--------|
| Backend | 5000 | http://localhost:5000 | Must be running |
| Frontend | 8000 | http://localhost:8000 | Must be running |

**Check ports:**
```cmd
netstat -ano | findstr :5000
netstat -ano | findstr :8000
```

**If ports are in use by other programs:**
- Close those programs
- Or change ports in code

---

## 🆘 Still Not Working?

### Check Firewall
Windows Firewall might be blocking connections:
1. Open Windows Defender Firewall
2. Click "Allow an app through firewall"
3. Find Python
4. Make sure both Private and Public are checked

### Check Antivirus
Some antivirus software blocks local connections:
- Temporarily disable antivirus
- Try again
- If it works, add Python to antivirus exceptions

### Use Different Browser
Try a different browser:
- Chrome
- Firefox
- Edge

### Check Python Version
```cmd
python --version
```
Should be Python 3.7 or higher

### Reinstall Flask-CORS
```cmd
pip uninstall flask-cors
pip install flask-cors
```

---

## ✅ Working Configuration

When everything is working, you should see:

**Terminal 1 (Backend):**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

**Terminal 2 (Frontend):**
```
Serving HTTP on :: port 8000 (http://[::]:8000/)
```

**Browser Console (F12):**
```
No errors
```

**Login Page:**
- Enter email: rohan.sharma@thapar.edu
- Enter password: password123
- Click Login
- Redirects to dashboard ✅

---

## 📞 Quick Commands

```cmd
# Check backend
curl http://localhost:5000/api/student/faculty

# Start backend
cd backend
python app.py

# Start frontend
cd frontend
python -m http.server 8000

# Test CORS
cd backend
python test_cors.py

# Diagnose issues
FIX_CORS_ISSUE.bat

# Complete restart
RUN_PROJECT.bat
```

---

## 🎯 Most Likely Causes

1. **Backend not running** (90% of cases)
   - Solution: `cd backend && python app.py`

2. **Backend needs restart** (5% of cases)
   - Solution: Stop (Ctrl+C) and start again

3. **Browser cache** (3% of cases)
   - Solution: Clear cache or use Incognito

4. **Wrong URL** (2% of cases)
   - Solution: Use `http://localhost:8000/login.html`

---

**Try the Quick Fix first, then work through the steps if needed!** 🚀
