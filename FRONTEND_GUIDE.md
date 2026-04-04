# Frontend Development Checklist

## 🎯 Overview

This checklist guides you through implementing the frontend for the Student-Faculty Portal v2.0. The backend is complete and ready - you just need to build the UI and connect to the APIs.

## ✅ Prerequisites

- [ ] Backend is running on `http://localhost:5000`
- [ ] You have test credentials (see QUICK_START.md)
- [ ] You've reviewed API_REFERENCE_V2.md
- [ ] You understand the system architecture (SYSTEM_ARCHITECTURE.md)

---

## 📋 Phase 1: Authentication (Priority: HIGH)

### Login Page
- [ ] Create login form (email + password)
- [ ] Call `POST /api/login` on form submit
- [ ] Store JWT token in localStorage/sessionStorage
- [ ] Store user info (user_id, name, role, class_name/faculty_id)
- [ ] Redirect to appropriate dashboard based on role
- [ ] Handle login errors (invalid credentials, server error)
- [ ] Add "Remember Me" functionality (optional)

### Logout Functionality
- [ ] Create logout button in navigation
- [ ] Call `POST /api/logout` (optional, token-based)
- [ ] Clear stored token and user info
- [ ] Redirect to login page

### Auth Helper Functions
- [ ] Create function to get stored token
- [ ] Create function to add token to API requests
- [ ] Create function to check if user is logged in
- [ ] Create function to redirect if not authenticated

**Test Cases:**
- [ ] Login with valid student credentials
- [ ] Login with valid faculty credentials
- [ ] Login with invalid credentials (should show error)
- [ ] Logout and verify token is cleared
- [ ] Try accessing protected pages without login (should redirect)

---

## 📋 Phase 2: Student Portal (Priority: HIGH)

### Student Dashboard
- [ ] Create dashboard layout with navigation
- [ ] Call `GET /api/student/dashboard`
- [ ] Display student info: name, class, branch, CGPA
- [ ] Display list of enrolled subjects
- [ ] Add navigation to: Marks, Attendance, Feedback, Alerts
- [ ] Style with cards/sections for better UX

### Student Marks Page
- [ ] Create subject selector dropdown
- [ ] Call `GET /api/student/marks?subject_id=X`
- [ ] Display marks in a table:
  - Assessment Type
  - Marks Obtained / Max Marks
  - Percentage
  - Class Average
- [ ] Add visual indicators (color coding for performance)
- [ ] Show "No marks uploaded yet" if empty
- [ ] Add chart/graph for visual comparison (optional)

### Student Attendance Page
- [ ] Create subject selector dropdown
- [ ] Call `GET /api/student/attendance?subject_id=X`
- [ ] Display attendance summary:
  - Percentage (with color coding)
  - Present count / Total count
- [ ] Display attendance records in a table/calendar
- [ ] Show "No attendance records" if empty
- [ ] Add date filter (optional)

### Student Alerts Page
- [ ] Call `GET /api/student/alerts`
- [ ] Display alerts with:
  - Alert type (Critical/Alert/Warning) with color coding
  - Message
  - Subject name
  - Timestamp
- [ ] Sort by date (newest first)
- [ ] Add filter by alert type (optional)
- [ ] Show "No alerts" if empty

### Student Feedback Page (Chat Interface)
- [ ] Call `GET /api/student/feedback/threads`
- [ ] Display list of subjects with:
  - Subject name
  - Message count
  - Last message time
- [ ] On subject click, open chat interface
- [ ] Call `GET /api/student/feedback?subject_id=X`
- [ ] Display chat messages:
  - Student messages on right (blue)
  - Faculty messages on left (gray)
  - Show sender name and timestamp
  - Scroll to bottom automatically
- [ ] Create message input box at bottom
- [ ] Call `POST /api/student/feedback` on send
- [ ] Append new message to chat immediately
- [ ] Implement auto-refresh (poll every 3-5 seconds)
- [ ] Show faculty name at top of chat
- [ ] Add "No messages yet" if thread is empty

**Test Cases:**
- [ ] View dashboard with all student info
- [ ] View marks for each subject
- [ ] View attendance for each subject
- [ ] View all alerts
- [ ] Send feedback message to faculty
- [ ] Receive faculty reply (test with another browser/incognito)
- [ ] Verify real-time updates work

---

## 📋 Phase 3: Faculty Portal (Priority: HIGH)

### Faculty Dashboard
- [ ] Create dashboard layout with navigation
- [ ] Call `GET /api/faculty/dashboard`
- [ ] Display faculty info: name, department, designation
- [ ] Display list of classes taught
- [ ] Display total student count
- [ ] Add navigation to: My Classes, Add Marks, Marks Report, Attendance, Feedback

### Faculty My Classes Page
- [ ] Call `GET /api/faculty/classes`
- [ ] Display classes as cards/list:
  - Class name (2Q11, 2Q12, etc.)
  - Student count
- [ ] On class click, show students
- [ ] Call `GET /api/faculty/class/students?class_name=X`
- [ ] Display students in a table:
  - Name
  - Email
  - CGPA
- [ ] Add search/filter functionality (optional)

### Faculty Add Marks Page
- [ ] Create class selector dropdown
- [ ] Call `GET /api/faculty/subjects?class_name=X`
- [ ] Create subject selector dropdown
- [ ] Call `GET /api/faculty/class/students?class_name=X`
- [ ] Display students in a table
- [ ] For each student, add marks entry form:
  - Assessment type dropdown (MST, EST, Assignment, Quiz)
  - Marks obtained input
  - Max marks input
  - Save button
- [ ] Call `POST /api/faculty/marks` on save
- [ ] Show success/error message
- [ ] Load existing marks if available
- [ ] Allow bulk entry (optional)

### Faculty Marks Report Page
- [ ] Create class selector dropdown
- [ ] Create subject selector dropdown
- [ ] Call `GET /api/faculty/marks/report?class_name=X&subject_id=Y`
- [ ] Display statistics in cards:
  - Highest marks per assessment
  - Lowest marks per assessment
  - Average marks per assessment
- [ ] Create bar/line chart showing comparison
- [ ] Use Chart.js or similar library
- [ ] Add export to PDF/Excel (optional)

### Faculty Attendance Page
- [ ] Create class selector dropdown
- [ ] Create subject selector dropdown
- [ ] Create date picker
- [ ] Call `GET /api/faculty/attendance?class_name=X&subject_id=Y&date=Z`
- [ ] Display students with Present/Absent radio buttons
- [ ] Call `POST /api/faculty/attendance` on submit
- [ ] Show success message
- [ ] Add "Mark All Present" button (optional)
- [ ] Show attendance summary (without date parameter)

### Faculty Feedback Page (Chat Interface)
- [ ] Create class selector dropdown
- [ ] Create subject selector dropdown
- [ ] Call `GET /api/faculty/feedback/students?class_name=X&subject_id=Y`
- [ ] Display list of students with:
  - Name
  - Message count
  - Last message time
- [ ] On student click, open chat interface
- [ ] Call `GET /api/faculty/feedback?student_id=X&subject_id=Y`
- [ ] Display chat messages:
  - Faculty messages on right (blue)
  - Student messages on left (gray)
  - Show sender name and timestamp
  - Scroll to bottom automatically
- [ ] Create message input box at bottom
- [ ] Call `POST /api/faculty/feedback` on send
- [ ] Append new message to chat immediately
- [ ] Implement auto-refresh (poll every 3-5 seconds)
- [ ] Show student name and class at top of chat
- [ ] Add "No messages yet" if thread is empty

**Test Cases:**
- [ ] View dashboard with faculty info
- [ ] View all classes taught
- [ ] View students in each class
- [ ] Add marks for students
- [ ] Update existing marks
- [ ] View marks report with graphs
- [ ] Mark attendance for a class
- [ ] Send feedback message to student
- [ ] Receive student message (test with another browser)
- [ ] Verify real-time updates work

---

## 📋 Phase 4: UI/UX Enhancements (Priority: MEDIUM)

### Navigation
- [ ] Create responsive navigation bar
- [ ] Show user name and role in header
- [ ] Add logout button
- [ ] Highlight active page
- [ ] Make mobile-friendly (hamburger menu)

### Loading States
- [ ] Add loading spinners for API calls
- [ ] Show skeleton screens while loading
- [ ] Disable buttons during submission

### Error Handling
- [ ] Display user-friendly error messages
- [ ] Handle network errors gracefully
- [ ] Show retry option on failure
- [ ] Log errors to console for debugging

### Notifications
- [ ] Add toast/snackbar for success messages
- [ ] Show notification badge for new feedback messages
- [ ] Add sound notification (optional)

### Responsive Design
- [ ] Test on mobile devices
- [ ] Test on tablets
- [ ] Test on different screen sizes
- [ ] Ensure tables are scrollable on small screens

### Accessibility
- [ ] Add proper labels to form inputs
- [ ] Ensure keyboard navigation works
- [ ] Add ARIA attributes
- [ ] Test with screen reader (optional)

---

## 📋 Phase 5: Advanced Features (Priority: LOW)

### Real-Time Updates
- [ ] Implement WebSocket for feedback (instead of polling)
- [ ] Show "typing..." indicator in chat
- [ ] Show online/offline status

### Data Visualization
- [ ] Add charts for marks comparison
- [ ] Add attendance calendar view
- [ ] Add progress bars for CGPA/attendance

### Bulk Operations
- [ ] Bulk marks upload via CSV
- [ ] Bulk attendance marking
- [ ] Export data to Excel/PDF

### Search & Filter
- [ ] Search students by name
- [ ] Filter marks by assessment type
- [ ] Filter attendance by date range
- [ ] Filter alerts by type

### Profile Management
- [ ] Allow users to change password
- [ ] Allow users to update profile info
- [ ] Add profile picture upload

---

## 🛠️ Technical Implementation Guide

### API Call Helper Function
```javascript
async function apiCall(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`http://localhost:5000${endpoint}`, options);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || 'API call failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
```

### Chat Auto-Refresh Example
```javascript
let chatInterval;

function startChatRefresh(subjectId) {
    chatInterval = setInterval(async () => {
        const data = await apiCall(`/api/student/feedback?subject_id=${subjectId}`);
        updateChatMessages(data.messages);
    }, 3000); // Poll every 3 seconds
}

function stopChatRefresh() {
    if (chatInterval) {
        clearInterval(chatInterval);
    }
}
```

### Chart.js Example for Marks Report
```javascript
const ctx = document.getElementById('marksChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['MST', 'EST', 'Assignment', 'Quiz'],
        datasets: [{
            label: 'Highest',
            data: [48, 92, 19, 10],
            backgroundColor: 'rgba(75, 192, 192, 0.6)'
        }, {
            label: 'Average',
            data: [36, 71, 16, 8],
            backgroundColor: 'rgba(255, 206, 86, 0.6)'
        }, {
            label: 'Lowest',
            data: [25, 45, 12, 5],
            backgroundColor: 'rgba(255, 99, 132, 0.6)'
        }]
    }
});
```

---

## 🎨 Design Guidelines

### Color Scheme
- **Primary**: #2196F3 (Blue)
- **Success**: #4CAF50 (Green)
- **Warning**: #FF9800 (Orange)
- **Danger**: #F44336 (Red)
- **Info**: #00BCD4 (Cyan)

### Alert Type Colors
- **Critical**: Red background
- **Alert**: Orange background
- **Warning**: Yellow background

### Chat Message Styling
- **Own messages**: Right-aligned, blue background
- **Other messages**: Left-aligned, gray background
- **Timestamp**: Small, gray text below message

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

---

## 🧪 Testing Checklist

### Functional Testing
- [ ] All API calls work correctly
- [ ] Data displays properly
- [ ] Forms submit successfully
- [ ] Error messages show correctly
- [ ] Navigation works on all pages

### Cross-Browser Testing
- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] API calls complete quickly
- [ ] No memory leaks in chat refresh
- [ ] Images/assets optimized

### Security Testing
- [ ] Token stored securely
- [ ] Protected routes require authentication
- [ ] No sensitive data in console logs
- [ ] XSS protection in place

---

## 📦 Recommended Libraries

### Essential
- **Chart.js**: For graphs and charts
- **Axios**: For API calls (alternative to fetch)
- **Moment.js**: For date formatting

### Optional
- **Socket.IO**: For real-time WebSocket communication
- **React/Vue/Angular**: For component-based architecture
- **Tailwind CSS**: For rapid UI development
- **SweetAlert2**: For beautiful alerts/modals

---

## 🚀 Deployment Checklist

- [ ] Update API base URL for production
- [ ] Minify JavaScript and CSS
- [ ] Optimize images
- [ ] Enable HTTPS
- [ ] Set up CORS properly
- [ ] Configure caching headers
- [ ] Test on production environment
- [ ] Set up error logging
- [ ] Create user documentation

---

## 📞 Need Help?

- **API Issues**: Check API_REFERENCE_V2.md
- **Architecture Questions**: Review SYSTEM_ARCHITECTURE.md
- **Setup Problems**: See IMPLEMENTATION_GUIDE_V2.md
- **Quick Start**: Read QUICK_START.md

---

**Remember**: The backend is complete and tested. Focus on creating a clean, user-friendly interface that connects to the existing APIs. Start with authentication and basic pages, then add advanced features.

Good luck! 🎉
