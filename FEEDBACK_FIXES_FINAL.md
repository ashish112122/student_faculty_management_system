# 🔧 Feedback System - Complete Fix Guide

## Problem Summary

**Issue 1:** Search button in faculty feedback doesn't work  
**Issue 2:** Messages don't send/receive (CRITICAL)

**Root Cause:** Backend API uses `feedback` table but database has `feedback_threads` and `feedback_messages` tables.

---

## Solution Overview

1. Remove search button from faculty portal (frontend fix)
2. Update backend API to use threading tables (backend fix)
3. Restart backend server
4. Test the system

---

## Fix 1: Remove Search Button (Easy - 2 minutes)

### File: `frontend/faculty_portal.html`

**Find this line (around line 248):**
```html
<input type="text" id="student-search-feedback" class="search-chat-input" placeholder="Search students..." oninput="filterFeedbackStudents(this.value)">
```

**Action:** DELETE that entire line

**Save the file.**

✅ Done! Search button removed.

---

## Fix 2: Update Backend API (Complex - Needs careful replacement)

### The Problem:
Backend code references `feedback` table which doesn't exist.  
Database has `feedback_threads` and `feedback_messages` tables.

### The Solution:
Replace feedback table queries with threading table queries.

### Key Changes Needed:

1. **Get messages:** Query `feedback_messages` joined with `feedback_threads`
2. **Send messages:** Insert into `feedback_messages`, create thread if needed
3. **Thread management:** Use `feedback_threads` table

---

## Detailed Backend Changes

### Change 1: Student Get Messages
**File:** `backend/app.py`  
**Function:** `get_student_feedback_thread` (around line 345)

**Replace this query:**
```python
cursor.execute("""
    SELECT feedback_id, sender_role, message, is_read, created_at, 
           attachment_path, attachment_name, attachment_type
    FROM feedback
    WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
    ORDER BY created_at ASC
""", {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
```

**With this:**
```python
# Get thread first
cursor.execute("""
    SELECT thread_id FROM feedback_threads
    WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
""", {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})

thread = cursor.fetchone()
if not thread:
    return jsonify([])

thread_id = thread[0]

# Get messages
cursor.execute("""
    SELECT message_id, sender_role, message, is_read, created_at, 
           attachment_path, attachment_name, attachment_type
    FROM feedback_messages
    WHERE thread_id = :thread_id
    ORDER BY created_at ASC
""", {'thread_id': thread_id})
```

**Also update the UPDATE query:**
```python
cursor.execute("""
    UPDATE feedback_messages SET is_read = 1
    WHERE thread_id = :thread_id AND sender_role = 'faculty' AND is_read = 0
""", {'thread_id': thread_id})
```

---

### Change 2: Student Send Message
**File:** `backend/app.py`  
**Function:** `send_student_feedback` (around line 393)

**Replace the INSERT query:**
```python
cursor.execute("""
    INSERT INTO feedback (feedback_id, student_id, faculty_id, subject_id, sender_role, message, is_read, 
                         attachment_path, attachment_name, attachment_type)
    VALUES (feedback_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, 'student', :message, 0,
           :attachment_path, :attachment_name, :attachment_type)
""", {...})
```

**With this:**
```python
# Get or create thread
cursor.execute("""
    SELECT thread_id FROM feedback_threads
    WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id
""", {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})

thread = cursor.fetchone()
if thread:
    thread_id = thread[0]
else:
    # Create new thread
    cursor.execute("""
        INSERT INTO feedback_threads (thread_id, student_id, faculty_id, subject_id, initiated_by, created_at, last_message_at)
        VALUES (feedback_threads_seq.NEXTVAL, :student_id, :faculty_id, :subject_id, 'student', SYSDATE, SYSDATE)
    """, {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})
    cursor.execute("SELECT feedback_threads_seq.CURRVAL FROM dual")
    thread_id = cursor.fetchone()[0]

# Insert message
cursor.execute("""
    INSERT INTO feedback_messages (message_id, thread_id, sender_id, sender_role, message, is_read, created_at,
                                  attachment_path, attachment_name, attachment_type)
    VALUES (feedback_messages_seq.NEXTVAL, :thread_id, :sender_id, 'student', :message, 0, SYSDATE,
           :attachment_path, :attachment_name, :attachment_type)
""", {
    'thread_id': thread_id,
    'sender_id': request.user_id,
    'message': message,
    'attachment_path': attachment_path,
    'attachment_name': attachment_name,
    'attachment_type': attachment_type
})

# Update thread
cursor.execute("""
    UPDATE feedback_threads SET last_message_at = SYSDATE WHERE thread_id = :thread_id
""", {'thread_id': thread_id})
```

---

### Change 3: Faculty Get Messages
**File:** `backend/app.py`  
**Function:** `get_faculty_feedback_thread` (around line 704)

**Same changes as Student Get Messages** (use feedback_threads and feedback_messages)

---

### Change 4: Faculty Send Message
**File:** `backend/app.py`  
**Function:** `send_faculty_feedback` (around line 752)

**Same changes as Student Send Message** (use feedback_threads and feedback_messages, but initiated_by = 'faculty')

---

### Change 5: Faculty Get Threads List
**File:** `backend/app.py`  
**Function:** `get_faculty_feedback_threads` (around line 663)

**Replace the query:**
```python
cursor.execute("""
    SELECT DISTINCT s.student_id, s.name, s.class_name, sub.subject_id, sub.subject_name,
           (SELECT COUNT(*) FROM feedback WHERE student_id = s.student_id AND faculty_id = :faculty_id 
            AND subject_id = sub.subject_id AND sender_role = 'student' AND is_read = 0) as unread_count
    FROM feedback f
    JOIN students s ON f.student_id = s.student_id
    JOIN subjects sub ON f.subject_id = sub.subject_id
    WHERE f.faculty_id = :faculty_id
    ORDER BY s.name
""", {'faculty_id': faculty_id})
```

**With this:**
```python
cursor.execute("""
    SELECT DISTINCT s.student_id, s.name, s.class_name, sub.subject_id, sub.subject_name,
           (SELECT COUNT(*) FROM feedback_messages fm 
            JOIN feedback_threads ft ON fm.thread_id = ft.thread_id
            WHERE ft.student_id = s.student_id AND ft.faculty_id = :faculty_id 
            AND ft.subject_id = sub.subject_id AND fm.sender_role = 'student' AND fm.is_read = 0) as unread_count
    FROM feedback_threads ft
    JOIN students s ON ft.student_id = s.student_id
    JOIN subjects sub ON ft.subject_id = sub.subject_id
    WHERE ft.faculty_id = :faculty_id
    ORDER BY s.name
""", {'faculty_id': faculty_id})
```

---

### Change 6: Download Attachment
**File:** `backend/app.py`  
**Function:** `download_attachment` (around line 1038)

**Change parameter from `feedback_id` to `message_id`:**
```python
@app.route('/api/feedback/attachment/<int:message_id>', methods=['GET'])
@token_required
def download_attachment(message_id):
    # ...
    cursor.execute("""
        SELECT attachment_path, attachment_name 
        FROM feedback_messages 
        WHERE message_id = :message_id
    """, {'message_id': message_id})
```

---

## After Making Changes

### Step 1: Save all files
- `frontend/faculty_portal.html` (search button removed)
- `backend/app.py` (all 6 changes made)

### Step 2: Restart Backend
```
Close backend window
Double-click: START_BACKEND.bat
```

### Step 3: Test
1. Login as student
2. Feedback → Select teacher → Send message
3. Message should appear immediately
4. Login as faculty
5. Feedback → Select batch → Select student
6. Message from student should appear
7. Reply to message
8. Login as student again
9. Faculty reply should appear

---

## Quick Verification

**Check if tables exist:**
```
python backend/check_feedback_threading.py
```

Should show:
- ✅ FEEDBACK_THREADS table exists
- ✅ FEEDBACK_MESSAGES table exists
- ✅ Sample data present

---

## If You Need Help

The changes are complex. If you want:
1. **Automated fix:** I can create a script to do it
2. **Step-by-step:** I can guide you through each change
3. **Complete file:** I can provide a fully fixed app.py

Let me know which approach you prefer!

---

**Status:** Fixes documented, ready to apply  
**Complexity:** Medium (6 functions to update)  
**Time:** 15-20 minutes manual editing
