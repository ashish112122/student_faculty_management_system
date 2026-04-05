const API_BASE = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');
    if (token) {
        if (role === 'student') {
            loadStudentDashboard();
        } else if (role === 'faculty') {
            loadFacultyDashboard();
        }
    }
});

// Login
if (document.getElementById('login-form')) {
    document.getElementById('login-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const role = document.getElementById('role').value;
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem('token', data.token);
            localStorage.setItem('role', data.role);
            window.location.href = data.role === 'student' ? 'student_dashboard.html' : 'faculty_dashboard.html';
        } else {
            alert(data.message);
        }
    });
}

// Register
if (document.getElementById('register-form')) {
    document.getElementById('register-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const department_id = document.getElementById('department').value;
        const res = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, name, role: 'student', department_id })
        });
        const data = await res.json();
        alert(data.message);
    });
}

// Logout
document.getElementById('logout')?.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = 'login.html';
});

// Load Student Dashboard
async function loadStudentDashboard() {
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_BASE}/student/dashboard`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    document.getElementById('semester').textContent = data.semester;
    document.getElementById('cgpa').textContent = data.cgpa;
    document.getElementById('credits').textContent = data.credits;
    // Populate marks table and chart
    const marksTable = document.getElementById('marks-table');
    marksTable.innerHTML = '<tr><th>Subject</th><th>Marks</th><th>Grade</th></tr>';
    data.marks.forEach(m => {
        marksTable.innerHTML += `<tr><td>${m[0]}</td><td>${m[1]}</td><td>${m[2]}</td></tr>`;
    });
    // Chart
    const ctx = document.getElementById('marks-chart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.marks.map(m => m[0]),
            datasets: [{
                label: 'Marks',
                data: data.marks.map(m => m[1])
            }]
        }
    });
    // Attendance
    const attDiv = document.getElementById('attendance-bars');
    data.attendance.forEach(a => {
        attDiv.innerHTML += `<p>${a[0]}: <div class="progress-bar"><div class="progress-fill" style="width: ${a[1]}%"></div></div> ${a[1]}%</p>`;
    });
    // Alerts
    const alertsList = document.getElementById('alerts-list');
    data.alerts.forEach(a => {
        alertsList.innerHTML += `<li class="${a[1] ? '' : 'unread'}">${a[0]}</li>`;
    });
}

// Load Faculty Dashboard
async function loadFacultyDashboard() {
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_BASE}/faculty/dashboard`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    document.getElementById('department').textContent = data.department;
    const subjectsList = document.getElementById('subjects-list');
    data.subjects.forEach(s => {
        subjectsList.innerHTML += `<li>${s[0]}</li>`;
    });
}

// Add Marks
document.getElementById('marks-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const student_id = document.getElementById('student_id').value;
    const subject_id = document.getElementById('subject_id').value;
    const marks = document.getElementById('marks').value;
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_BASE}/faculty/add_marks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ student_id, subject_id, marks })
    });
    const data = await res.json();
    alert(data.message);
});

// Similar for attendance, feedback, etc.