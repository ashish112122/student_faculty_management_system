const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    
    await loadSubjects();
});

async function loadSubjects() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/subjects`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const subjects = await response.json();
        const subjectList = document.getElementById('subjectList');
        
        subjects.forEach(subject => {
            const card = document.createElement('div');
            card.className = 'subject-card';
            card.innerHTML = `<h3>${subject.subject_name}</h3>`;
            card.onclick = () => loadAttendance(subject.subject_id, subject.subject_name);
            subjectList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading subjects:', error);
    }
}

async function loadAttendance(subjectId, subjectName) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/attendance?subject_id=${subjectId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        document.getElementById('subjectList').style.display = 'none';
        document.getElementById('attendanceDetail').style.display = 'block';
        document.getElementById('subjectName').textContent = subjectName;
        
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        // Check if attendance is uploaded
        if (data.records.length === 0) {
            document.getElementById('attendancePercentage').textContent = 'N/A';
            document.getElementById('progressBar').style.width = '0%';
            tbody.innerHTML = '<tr><td colspan="2" style="text-align: center; padding: 40px; color: #999;">Attendance not uploaded yet by faculty</td></tr>';
            return;
        }
        
        const percentage = data.percentage;
        document.getElementById('attendancePercentage').textContent = `${percentage}%`;
        
        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = `${percentage}%`;
        progressBar.className = 'progress-fill';
        
        if (percentage < 50) {
            progressBar.classList.add('danger');
        } else if (percentage < 75) {
            progressBar.classList.add('warning');
        }
        
        data.records.forEach(record => {
            const row = document.createElement('tr');
            const statusClass = record.status === 'Present' ? 'status-present' : 'status-absent';
            row.innerHTML = `
                <td>${record.date}</td>
                <td class="${statusClass}">${record.status}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

function backToSubjects() {
    document.getElementById('attendanceDetail').style.display = 'none';
    document.getElementById('subjectList').style.display = 'grid';
}
