# Feedback Threading System Implementation Guide

## Overview
This document describes the updated feedback/chat system that supports:
- Both students and faculty can initiate conversations
- Multiple independent threads between same student-faculty pair
- Thread-based messaging with proper organization
- Search functionality
- "New Chat" option for both sides

## Database Schema Changes

### New Tables

#### 1. feedback_threads
Stores conversation metadata:
```sql
CREATE TABLE feedback_threads (
    thread_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    faculty_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    thread_title VARCHAR2(200),
    initiated_by VARCHAR2(20) NOT NULL CHECK (initiated_by IN ('student', 'faculty')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
```

#### 2. feedback_messages
Stores individual messages:
```sql
CREATE TABLE feedback_messages (
    message_id NUMBER PRIMARY KEY,
    thread_id NUMBER NOT NULL,
    sender_id NUMBER NOT NULL,
    sender_role VARCHAR2(20) NOT NULL CHECK (sender_role IN ('student', 'faculty')),
    message CLOB NOT NULL,
    is_read NUMBER(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attachment_path VARCHAR2(500),
    attachment_name VARCHAR2(200),
    attachment_type VARCHAR2(50),
    FOREIGN KEY (thread_id) REFERENCES feedback_threads(thread_id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
);
```

## API Endpoints

### Student APIs

#### 1. Get All Threads
```
GET /api/student/feedback/threads
Headers: Authorization: Bearer <token>
Response: Array of thread objects with unread counts
```

#### 2. Get Faculty List (for starting new thread)
```
GET /api/student/feedback/faculty_list
Headers: Authorization: Bearer <token>
Response: Array of faculty teaching student's class
```

#### 3. Create New Thread
```
POST /api/student/feedback/create_thread
Headers: Authorization: Bearer <token>
Body: {
    "faculty_id": 1,
    "subject_id": 2,
    "thread_title": "Question about Assignment",
    "message": "Initial message (optional)"
}
Response: { "message": "Thread created", "thread_id": 123 }
```

#### 4. Get Thread Messages
```
GET /api/feedback/thread/<thread_id>/messages
Headers: Authorization: Bearer <token>
Response: Array of messages in chronological order
```

#### 5. Send Message to Thread
```
POST /api/feedback/thread/<thread_id>/send
Headers: Authorization: Bearer <token>
Body: {
    "message": "Message text"
}
OR multipart/form-data with attachment
Response: { "message": "Message sent successfully" }
```

### Faculty APIs

#### 1. Get All Threads
```
GET /api/faculty/feedback/threads
Headers: Authorization: Bearer <token>
Response: Array of thread objects with student info and unread counts
```

#### 2. Get Student List (for starting new thread)
```
GET /api/faculty/feedback/student_list?subject_id=1&class_name=2Q34
Headers: Authorization: Bearer <token>
Response: Array of students in faculty's classes
```

#### 3. Create New Thread
```
POST /api/faculty/feedback/create_thread
Headers: Authorization: Bearer <token>
Body: {
    "student_id": 5,
    "subject_id": 2,
    "thread_title": "Regarding your performance",
    "message": "Initial message (optional)"
}
Response: { "message": "Thread created", "thread_id": 124 }
```

#### 4. Get Thread Messages (same as student)
```
GET /api/feedback/thread/<thread_id>/messages
```

#### 5. Send Message (same as student)
```
POST /api/feedback/thread/<thread_id>/send
```

### Common APIs

#### Search Threads
```
GET /api/feedback/search?q=assignment
Headers: Authorization: Bearer <token>
Response: Array of matching threads
```

## Frontend Implementation

### Student Portal

#### Thread List View
```javascript
// Load all threads
async function loadThreads() {
    const response = await fetch(`${API_URL}/student/feedback/threads`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const threads = await response.json();
    // Display threads with:
    // - Thread title
    // - Faculty name
    // - Subject name
    // - Last message time
    // - Unread count badge
}
```

#### New Thread Button
```javascript
// Show faculty list
async function showNewThreadDialog() {
    const response = await fetch(`${API_URL}/student/feedback/faculty_list`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const faculty = await response.json();
    // Display faculty list grouped by subject
    // User selects faculty + subject
    // User enters thread title and optional first message
}

// Create thread
async function createThread(facultyId, subjectId, title, message) {
    const response = await fetch(`${API_URL}/student/feedback/create_thread`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            faculty_id: facultyId,
            subject_id: subjectId,
            thread_title: title,
            message: message
        })
    });
    const result = await response.json();
    // Open the new thread
    openThread(result.thread_id);
}
```

#### Chat View
```javascript
// Load messages
async function loadMessages(threadId) {
    const response = await fetch(`${API_URL}/feedback/thread/${threadId}/messages`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const messages = await response.json();
    // Display messages with:
    // - Sender name
    // - Message text
    // - Timestamp
    // - Attachment (if any)
    // - Align left for received, right for sent
}

// Send message
async function sendMessage(threadId, message, attachment) {
    if (attachment) {
        const formData = new FormData();
        formData.append('message', message);
        formData.append('attachment', attachment);
        
        await fetch(`${API_URL}/feedback/thread/${threadId}/send`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });
    } else {
        await fetch(`${API_URL}/feedback/thread/${threadId}/send`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
    }
    // Reload messages
    loadMessages(threadId);
}
```

#### Search
```javascript
async function searchThreads(keyword) {
    const response = await fetch(`${API_URL}/feedback/search?q=${encodeURIComponent(keyword)}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const results = await response.json();
    // Display search results
}
```

### Faculty Portal

#### Thread List View (similar to student)
```javascript
async function loadThreads() {
    const response = await fetch(`${API_URL}/faculty/feedback/threads`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const threads = await response.json();
    // Display threads with:
    // - Thread title
    // - Student name + roll number
    // - Class name
    // - Subject name
    // - Last message time
    // - Unread count badge
}
```

#### New Thread Button
```javascript
// Show student list
async function showNewThreadDialog(subjectId, className) {
    const response = await fetch(
        `${API_URL}/faculty/feedback/student_list?subject_id=${subjectId}&class_name=${className}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
    );
    const students = await response.json();
    // Display student list with:
    // - Name
    // - Roll number
    // - Class
    // - Subject
}

// Create thread
async function createThread(studentId, subjectId, title, message) {
    const response = await fetch(`${API_URL}/faculty/feedback/create_thread`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            student_id: studentId,
            subject_id: subjectId,
            thread_title: title,
            message: message
        })
    });
    const result = await response.json();
    openThread(result.thread_id);
}
```

## UI Components

### Thread List Sidebar
```html
<div class="thread-sidebar">
    <div class="sidebar-header">
        <h3>Conversations</h3>
        <button onclick="showNewThreadDialog()">+ New Chat</button>
    </div>
    <div class="search-box">
        <input type="text" placeholder="Search..." oninput="searchThreads(this.value)">
    </div>
    <div class="thread-list" id="threadList">
        <!-- Thread items -->
    </div>
</div>
```

### Thread Item
```html
<div class="thread-item" onclick="openThread(threadId)">
    <div class="thread-header">
        <span class="thread-title">Assignment Question</span>
        <span class="thread-time">2 hours ago</span>
    </div>
    <div class="thread-info">
        <span class="participant-name">Dr. Rajesh Kumar</span>
        <span class="subject-name">Data Structures</span>
    </div>
    <span class="unread-badge">3</span>
</div>
```

### Chat View
```html
<div class="chat-view">
    <div class="chat-header">
        <button onclick="backToThreadList()">← Back</button>
        <div class="chat-title">
            <h3 id="threadTitle">Assignment Question</h3>
            <p id="chatInfo">Dr. Rajesh Kumar • Data Structures</p>
        </div>
    </div>
    <div class="messages-container" id="messagesContainer">
        <!-- Messages -->
    </div>
    <div class="message-input">
        <input type="file" id="attachmentInput" style="display:none">
        <button onclick="document.getElementById('attachmentInput').click()">📎</button>
        <textarea id="messageText" placeholder="Type a message..."></textarea>
        <button onclick="sendMessage()">Send</button>
    </div>
</div>
```

### Message Bubble
```html
<div class="message sent">
    <div class="message-header">
        <span class="sender-name">You</span>
        <span class="message-time">10:30 AM</span>
    </div>
    <div class="message-text">Can you explain the concept again?</div>
    <div class="message-attachment" v-if="hasAttachment">
        <a href="#">📎 document.pdf</a>
    </div>
</div>
```

## Migration Steps

### 1. Database Migration
```sql
-- Run schema_feedback_threads.sql
-- This creates new tables and sequences

-- Migrate existing data (if any)
-- This is optional if starting fresh
```

### 2. Backend Updates
```python
# In backend/app.py, add:
from feedback_api import register_feedback_routes

# After app initialization:
register_feedback_routes(app, get_db_connection, token_required)
```

### 3. Frontend Updates
- Update feedback.html with new UI
- Update feedback.js with new API calls
- Add thread list view
- Add new thread dialog
- Add search functionality

## Testing Checklist

### Student Tests
- [ ] View all threads
- [ ] Create new thread with faculty
- [ ] Send message in thread
- [ ] Receive message from faculty
- [ ] Upload attachment
- [ ] Download attachment
- [ ] Search threads
- [ ] Mark messages as read
- [ ] View unread count

### Faculty Tests
- [ ] View all threads
- [ ] Create new thread with student
- [ ] Send message in thread
- [ ] Receive message from student
- [ ] Upload attachment
- [ ] Download attachment
- [ ] Search threads
- [ ] Filter students by class/subject
- [ ] View student info (name, roll, class)
- [ ] Mark messages as read
- [ ] View unread count

### Edge Cases
- [ ] Multiple threads between same student-faculty pair
- [ ] Thread with no messages
- [ ] Long messages (CLOB handling)
- [ ] Large attachments
- [ ] Concurrent messages
- [ ] Thread access control (unauthorized access)

## Benefits of New System

1. **Better Organization**: Threads keep conversations organized by topic
2. **Flexibility**: Both sides can initiate conversations
3. **Multiple Conversations**: Same pair can have multiple independent chats
4. **Search**: Easy to find past conversations
5. **Scalability**: Better performance with indexed queries
6. **User Experience**: Similar to modern chat apps (WhatsApp, Slack)

## Next Steps

1. Run database migration script
2. Update backend with new API endpoints
3. Update frontend with new UI components
4. Test thoroughly
5. Deploy to production

---

**Implementation Status**: Ready for development
**Estimated Time**: 4-6 hours
**Priority**: High
