# 🔧 FRONTEND TROUBLESHOOTING GUIDE

## ✅ CURRENT STATUS

**Backend:** ✅ Running on http://localhost:5000  
**Frontend:** ✅ Running on http://localhost:8000  
**Login Page:** ✅ Accessible at http://localhost:8000/login_test.html

Both servers are now running successfully!

---

## 🌐 HOW TO ACCESS FRONTEND

### Method 1: Direct URL (Recommended)
Copy and paste this in your browser:
```
http://localhost:8000/login_test.html
```

### Method 2: Command Line
Run this command:
```powershell
start http://localhost:8000/login_test.html
```

### Method 3: Browser Address Bar
1. Open your browser (Chrome, Edge, Firefox)
2. Type in address bar: `localhost:8000/login_test.html`
3. Press Enter

---

## 🔍 COMMON ISSUES & SOLUTIONS

### Issue 1: "This site can't be reached"

**Cause:** Frontend server not running

**Solution:**
```powershell
# Start frontend server
cd frontend
python -m http.server 8000
```

Or double-click: `START_FRONTEND.bat`

**Verify it's running:**
```powershell
# Should show "Serving HTTP on..."
```

---

### Issue 2: "Connection refused" or "ERR_CONNECTION_REFUSED"

**Cause:** Port 8000 is blocked or already in use

**Solution 1: Check if port is in use**
```powershell
netstat -ano | findstr :8000
```

**Solution 2: Kill the process**
```powershell
# Find PID from above command, then:
taskkill /PID <PID> /F
```

**Solution 3: Use different port**
```powershell
cd frontend
python -m http.server 8080
# Then access: http://localhost:8080/login_test.html
```

---

### Issue 3: Page loads but login doesn't work

**Cause:** Backend not running

**Solution:**
```powershell
# Start backend
cd backend
python app.py
```

Or double-click: `START_BACKEND.bat`

**Verify backend:**
```
http://localhost:5000
```
Should show: "Backend running successfully"

---

### Issue 4: "Python not found"

**Cause:** Python not installed or not in PATH

**Solution:**
```powershell
# Check Python installation
python --version
```

If not found:
1. Install Python from python.org
2. Or use full path: `C:\Python313\python.exe -m http.server 8000`

---

### Issue 5: Blank page or "404 Not Found"

**Cause:** Wrong directory or file not found

**Solution:**
```powershell
# Make sure you're in the right directory
cd C:\Users\vansh\student_faculty_management_system\frontend

# Check if file exists
dir login_test.html

# Start server
python -m http.server 8000
```

---

### Issue 6: CSS not loading (page looks broken)

**Cause:** CSS file path incorrect

**Solution:**
Check if CSS file exists:
```powershell
dir css\login.css
```

If missing, the page will still work but look unstyled.

---

## 🚀 EASIEST SOLUTION - USE START_ALL.bat

Instead of troubleshooting, just use the automated script:

**Step 1:** Navigate to project folder
```
C:\Users\vansh\student_faculty_management_system\
```

**Step 2:** Double-click
```
START_ALL.bat
```

**Step 3:** Wait 5 seconds

**Step 4:** Browser opens automatically

**Done!** ✅

---

## 📊 VERIFY EVERYTHING IS WORKING

### Test 1: Backend
```
URL: http://localhost:5000
Expected: "Backend running successfully"
```

### Test 2: Frontend
```
URL: http://localhost:8000/login_test.html
Expected: Login page appears
```

### Test 3: Connection Test
```
URL: http://localhost:8000/test_backend_connection.html
Expected: Shows backend status
```

### Test 4: Login
```
Email: rohan.sharma.2q34.3@thapar.edu
Password: pass123
Expected: Redirects to student dashboard
```

---

## 🔄 RESTART EVERYTHING

If nothing works, restart everything:

**Step 1: Stop all processes**
- Close all command prompt windows
- Or press Ctrl+C in each window

**Step 2: Start fresh**
```powershell
# Double-click this file
START_ALL.bat
```

**Step 3: Wait 5 seconds**

**Step 4: Try again**

---

## 🌐 ALTERNATIVE: Use File Protocol (Not Recommended)

If HTTP server doesn't work, you can try file protocol:

**Open directly:**
```
file:///C:/Users/vansh/student_faculty_management_system/frontend/login_test.html
```

**⚠️ Warning:** This may cause CORS issues with backend.

**Better solution:** Use HTTP server (port 8000)

---

## 📱 BROWSER-SPECIFIC ISSUES

### Chrome/Edge
- Usually works best
- No special configuration needed

### Firefox
- May have stricter CORS policies
- Try Chrome/Edge if issues persist

### Internet Explorer
- Not supported
- Use Chrome, Edge, or Firefox

---

## 🔍 DETAILED DIAGNOSTICS

### Check if servers are running:

**Backend:**
```powershell
# Should show process on port 5000
netstat -ano | findstr :5000
```

**Frontend:**
```powershell
# Should show process on port 8000
netstat -ano | findstr :8000
```

### Check if ports are accessible:

**Backend:**
```powershell
Test-NetConnection -ComputerName localhost -Port 5000
```

**Frontend:**
```powershell
Test-NetConnection -ComputerName localhost -Port 8000
```

### Check firewall:

```powershell
# Allow Python through firewall
netsh advfirewall firewall add rule name="Python HTTP Server" dir=in action=allow program="C:\Python313\python.exe" enable=yes
```

---

## 🎯 QUICK FIX CHECKLIST

- [ ] Backend running? Check http://localhost:5000
- [ ] Frontend running? Check http://localhost:8000/login_test.html
- [ ] Python installed? Run `python --version`
- [ ] In correct directory? Check path
- [ ] Ports available? Check with netstat
- [ ] Firewall blocking? Check Windows Firewall
- [ ] Browser working? Try different browser

---

## 💡 PRO TIPS

### Tip 1: Keep terminals open
Don't close the command prompt windows while using the system.

### Tip 2: Use Chrome DevTools
Press F12 to see console errors and network requests.

### Tip 3: Check browser console
Look for JavaScript errors or failed API calls.

### Tip 4: Clear browser cache
Press Ctrl+Shift+Delete and clear cache.

### Tip 5: Use incognito mode
Test in incognito/private browsing mode.

---

## 🆘 STILL NOT WORKING?

### Last Resort Solutions:

**Solution 1: Restart computer**
Sometimes Windows needs a restart to free up ports.

**Solution 2: Use different ports**
```powershell
# Backend on 5001
cd backend
python app.py --port 5001

# Frontend on 8001
cd frontend
python -m http.server 8001
```

Then update frontend to use port 5001 for backend.

**Solution 3: Check antivirus**
Temporarily disable antivirus and try again.

**Solution 4: Run as administrator**
Right-click START_ALL.bat → "Run as administrator"

---

## 📞 SUPPORT COMMANDS

### Get system info:
```powershell
python --version
netstat -ano | findstr :5000
netstat -ano | findstr :8000
Get-Process python
```

### Kill all Python processes:
```powershell
Get-Process python | Stop-Process -Force
```

### Restart servers:
```powershell
# Stop all
Get-Process python | Stop-Process -Force

# Start fresh
cd C:\Users\vansh\student_faculty_management_system
START_ALL.bat
```

---

## ✅ SUCCESS INDICATORS

When everything is working, you should see:

**Terminal 1 (Backend):**
```
* Running on http://127.0.0.1:5000
* Debugger is active!
```

**Terminal 2 (Frontend):**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

**Browser:**
```
Login page loads at http://localhost:8000/login_test.html
Can login successfully
Dashboard shows data
```

---

## 🎉 CURRENT STATUS

✅ **Backend:** Running on port 5000  
✅ **Frontend:** Running on port 8000  
✅ **Login Page:** http://localhost:8000/login_test.html  
✅ **Test Page:** http://localhost:8000/test_backend_connection.html

**Everything is working!** Just open the URL in your browser.

---

**Last Updated:** April 7, 2026  
**Status:** ✅ BOTH SERVERS RUNNING  
**Action:** Open http://localhost:8000/login_test.html in browser
