const API_URL = 'http://localhost:5000/api';
let currentChart = null;

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
            card.onclick = () => loadMarks(subject.subject_id, subject.subject_name);
            subjectList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading subjects:', error);
    }
}

async function loadMarks(subjectId, subjectName) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/marks?subject_id=${subjectId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        document.getElementById('subjectList').style.display = 'none';
        document.getElementById('marksDetail').style.display = 'block';
        document.getElementById('subjectName').textContent = subjectName;
        
        const tbody = document.getElementById('marksTableBody');
        tbody.innerHTML = '';
        
        // Check if marks are uploaded
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 40px; color: #999;">Marks not uploaded yet by faculty</td></tr>';
            
            // Hide chart
            const chartCanvas = document.getElementById('marksChart');
            if (chartCanvas) {
                chartCanvas.style.display = 'none';
            }
            return;
        }
        
        // Show chart
        const chartCanvas = document.getElementById('marksChart');
        if (chartCanvas) {
            chartCanvas.style.display = 'block';
        }
        
        const labels = [];
        const studentMarks = [];
        const classAverage = [];
        
        data.forEach(mark => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${mark.assessment_type}</td>
                <td>${mark.marks_obtained}</td>
                <td>${mark.class_average}</td>
            `;
            tbody.appendChild(row);
            
            labels.push(mark.assessment_type);
            studentMarks.push(mark.marks_obtained);
            classAverage.push(mark.class_average);
        });
        
        renderChart(labels, studentMarks, classAverage);
    } catch (error) {
        console.error('Error loading marks:', error);
    }
}

function backToSubjects() {
    document.getElementById('marksDetail').style.display = 'none';
    document.getElementById('subjectList').style.display = 'grid';
    
    // Destroy chart if exists
    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }
}

function renderChart(labels, studentMarks, classAverage) {
    if (currentChart) {
        currentChart.destroy();
    }
    
    const ctx = document.getElementById('marksChart').getContext('2d');
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Your Marks',
                data: studentMarks,
                backgroundColor: '#667eea'
            }, {
                label: 'Class Average',
                data: classAverage,
                backgroundColor: '#f39c12'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
