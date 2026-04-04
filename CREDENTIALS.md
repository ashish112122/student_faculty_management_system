# Working Test Credentials

## ✅ Faculty Login Credentials

### Dr. Rajesh Kumar (Teaches DBMS)
```
Email: dr.rajesh@thaparfac.edu
Password: pass123
```
**Classes:** 2Q11, 2Q12  
**Subject:** Database Management Systems

---

### Prof. Meena Sharma (Teaches OS)
```
Email: prof.meena@thaparfac.edu
Password: pass123
```
**Classes:** 2Q11  
**Subject:** Operating Systems

---

### Dr. Suresh Patel (Teaches Networks)
```
Email: dr.suresh@thaparfac.edu
Password: pass123
```
**Classes:** 2Q12  
**Subject:** Computer Networks

---

### Prof. Kavita Singh (Teaches Software Engineering)
```
Email: prof.kavita@thaparfac.edu
Password: pass123
```
**Classes:** 2Q11, 2Q12  
**Subject:** Software Engineering

---

### Dr. Anil Verma (Teaches Data Structures)
```
Email: dr.anil@thaparfac.edu
Password: pass123
```
**Classes:** 2Q11, 2Q12  
**Subject:** Data Structures

---

## ✅ Student Login Credentials

### Class 2Q11 Students

```
Email: rohan.sharma@thapar.edu
Password: pass123
Name: Rohan Sharma
Class: 2Q11
```

```
Email: priya.patel@thapar.edu
Password: pass123
Name: Priya Patel
Class: 2Q11
```

```
Email: amit.kumar@thapar.edu
Password: pass123
Name: Amit Kumar
Class: 2Q11
```

---

## 🧪 Quick Test

### Test Faculty Login (API)
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dr.rajesh@thaparfac.edu","password":"pass123"}'
```

### Test Student Login (API)
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"rohan.sharma@thapar.edu","password":"pass123"}'
```

---

## 📊 Database Status

- **Faculty:** 5 users
- **Students:** 10 users (Class 2Q11 and 2Q12)
- **Subjects:** 5 subjects
- **Faculty-Class Assignments:** 8 assignments
- **Marks:** 200 records
- **Attendance:** 1,500 records
- **Alerts:** 11 records

---

## 🚀 Next Steps

1. **Start the backend server:**
   ```bash
   cd backend
   python app_v2.py
   ```
   Or run: `START_SERVER_V2.bat`

2. **Test login** with any of the credentials above

3. **Build frontend** using the API documentation in `API_REFERENCE_V2.md`

---

## ⚠️ Important Notes

- All passwords are `pass123` for demo purposes
- Faculty emails end with `@thaparfac.edu`
- Student emails end with `@thapar.edu`
- The backend is running on `http://localhost:5000`
- JWT tokens expire after 24 hours

---

**Status:** ✅ Database migrated and ready for use!
