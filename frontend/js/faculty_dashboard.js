const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    await loadFacultyData();
});

async function loadFacultyData() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/dashboard`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Faculty data loaded:', data);
        
        // Display faculty info
        document.getElementById('faculty-name').textContent = data.profile.name || 'N/A';
        document.getElementById('faculty-email').textContent = data.profile.email || 'N/A';
        document.getElementById('faculty-id').textContent = data.faculty_id || 'N/A';
        document.getElementById('faculty-dept').textContent = data.profile.department || 'N/A';
        
        // Display classes
        const classList = document.getElementById('classes-list');
        if (data.subjects && data.subjects.length > 0) {
            classList.innerHTML = data.subjects.map(subject => `
                <div class="class-item">
                    <div class="class-name">${subject.subject_name}</div>
                    <div class="class-students">${subject.student_count} students</div>
                </div>
            `).join('');
        } else {
            classList.innerHTML = '<p style="color:#999;font-size:13px">No classes assigned</p>';
        }
    } catch (error) {
        console.error('Error loading faculty data:', error);
        alert('Failed to load faculty data: ' + error.message + '. Please check console for details.');
    }
}

function logout() {
    localStorage.clear();
    window.location.href = '/login';
}
