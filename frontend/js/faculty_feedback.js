const API_URL = 'http://localhost:5000/api';
let selectedClassId = null;
let selectedClassName = null;
let selectedStudentId = null;
let selectedStudentName = null;
let currentView = 'class';
let refreshInterval = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    loadClasses();
});

async function loadClasses() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/dashboard`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Failed to load');
        
        const data = await response.json();
        const grid = document.getElementById('class-grid');
        
        if (!data.subjects || data.subjects.length === 0) {
            grid.innerHTML = '<p class="empty-message">No classes assigned</p>';
            return;
        }
        
        grid.innerHTML = data.subjects.map(subject => `
            <div class="card clickable" onclick="selectClass(${subject.subject_id}, '${escapeHtml(subject.subject_name)}')">
                <h3>${escapeHtml(subject.subject_name)}</h3>
                <p>${subject.subject_code || 'N/A'}</p>
                <p class="highlight">${subject.student_count} students</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('class-grid').innerHTML = '<p class="error-message">Failed to load classes</p>';
    }
}

async function selectClass(classId, className) {
    selectedClassId = classId;
    selectedClassName = className;
    currentView = 'student';
    
    document.getElementById('selected-class-name').textContent = className;
    document.getElementById('class-selection').style.display = 'none';
    document.getElementById('student-selection').style.display = 'block';
    
    await loadStudents();
}

async function loadStudents() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/students?subject_id=${selectedClassId}&exam_type=MST`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Failed to load');
        
        const data = await response.json();
        const list = document.getElementById('student-list');
        
        if (!data.students || data.students.length === 0) {
            list.innerHTML = '<p class="empty-message">No students enrolled</p>';
            return;
        }
        
        list.innerHTML = data.students.map(student => `
            <div class="list-item" onclick="selectStudent(${student.student_id}, '${escapeHtml(student.student_name)}')">
                <div>
                    <div class="item-title">${escapeHtml(student.student_name)}</div>
                    <div class="item-subtitle">ID: ${student.student_id}</div>
                </div>
                <div class="arrow">→</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('student-list').innerHTML = '<p class="error-message">Failed to load students</p>';
    }
}

async function selectStudent(studentId, studentName) {
    selectedStudentId = studentId;
    selectedStudentName = studentName;
    currentView = 'chat';
    
    document.getElementById('student-name').textContent = studentName;
    document.getElementById('chat-class-name').textContent = selectedClassName;
    document.getElementById('student-selection').style.display = 'none';
    document.getElementById('chat-view').style.display = 'block';
    
    await loadMessages();
    
    // Auto-refresh messages every 3 seconds
    if (refreshInterval) clearInterval(refreshInterval);
    refreshInterval = setInterval(loadMessages, 3000);
}

async function loadMessages() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/feedback?subject_id=${selectedClassId}&student_id=${selectedStudentId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Failed to load');
        
        const messages = await response.json();
        const container = document.getElementById('messages-container');
        
        if (messages.length === 0) {
            container.innerHTML = '<p class="empty-message">No messages yet</p>';
            return;
        }
        
        container.innerHTML = messages.map(msg => `
            <div class="message ${msg.sender_role}">
                <div class="message-header">
                    <strong>${msg.sender_name}</strong>
                    <span class="message-time">${msg.created_at}</span>
                </div>
                <div class="message-text">${escapeHtml(msg.message)}</div>
            </div>
        `).join('');
        
        container.scrollTop = container.scrollHeight;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function sendMessage() {
    const token = localStorage.getItem('token');
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    try {
        const response = await fetch(`${API_URL}/faculty/feedback`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                subject_id: selectedClassId,
                student_id: selectedStudentId,
                message: message
            })
        });
        
        if (response.ok) {
            input.value = '';
            await loadMessages();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function goBack() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
    
    if (currentView === 'chat') {
        currentView = 'student';
        document.getElementById('chat-view').style.display = 'none';
        document.getElementById('student-selection').style.display = 'block';
    } else if (currentView === 'student') {
        currentView = 'class';
        document.getElementById('student-selection').style.display = 'none';
        document.getElementById('class-selection').style.display = 'block';
    } else {
        window.location.href = '/faculty';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
