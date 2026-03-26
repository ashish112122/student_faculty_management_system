const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    
    if (!token || !userId) {
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/student/dashboard`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Unauthorized');
        }
        
        const data = await response.json();
        
        document.getElementById('studentName').textContent = data.name;
        document.getElementById('branch').textContent = data.branch;
        document.getElementById('year').textContent = data.year;
        document.getElementById('semester').textContent = data.semester;
        document.getElementById('section').textContent = data.section;
        document.getElementById('cgpa').textContent = data.cgpa;
        
        const subjectList = document.getElementById('subjectList');
        data.subjects.forEach(subject => {
            const li = document.createElement('li');
            li.textContent = subject;
            subjectList.appendChild(li);
        });
        
    } catch (error) {
        localStorage.clear();
        window.location.href = 'login.html';
    }
});

document.getElementById('toggleBtn').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

document.getElementById('logoutBtn').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    
    await fetch(`${API_URL}/logout`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    localStorage.clear();
    window.location.href = 'login.html';
});
