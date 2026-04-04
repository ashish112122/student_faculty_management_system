const API_URL = 'http://localhost:5000/api';
let marksChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    // Set up dynamic back button
    setupBackButton();
    
    await loadSubjects();
});

function setupBackButton() {
    const backBtn = document.querySelector('.header .back-btn');
    if (backBtn) {
        backBtn.onclick = function() {
            const marksDetail = document.getElementById('marksDetail');
            if (marksDetail && marksDetail.style.display !== 'none') {
                // If viewing marks detail, go back to subjects list
                backToSubjects();
            } else {
                // If viewing subjects list, go to dashboard
                window.location.href = '/student/dashboard';
            }
        };
    }
}

async function loadSubjects() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/subjects`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const subjects = await response.json();
        const subjectList = document.getElementById('subjectList');
        subjectList.innerHTML = '';
        
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
        if (!data || data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" style="text-align: center; padding: 40px; color: #999;">Marks not uploaded yet by faculty</td></tr>';
            // Hide chart if no data
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
        
        // Populate table
        data.forEach(mark => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${mark.assessment_type}</td>
                <td>${mark.marks_obtained} / ${mark.max_marks}</td>
                <td>${mark.class_average}</td>
            `;
            tbody.appendChild(row);
        });
        
        // Render chart
        renderMarksChart(data);
        
    } catch (error) {
        console.error('Error loading marks:', error);
    }
}

function renderMarksChart(marks) {
    const canvas = document.getElementById('marksChart');
    if (!canvas) return;
    
    // Destroy existing chart
    if (marksChart) {
        marksChart.destroy();
    }
    
    const labels = marks.map(m => m.assessment_type);
    const studentMarks = marks.map(m => m.marks_obtained);
    const classAverages = marks.map(m => m.class_average);
    
    marksChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Your Marks',
                    data: studentMarks,
                    backgroundColor: 'rgba(91, 106, 191, 0.8)',
                    borderColor: 'rgba(91, 106, 191, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Class Average',
                    data: classAverages,
                    backgroundColor: 'rgba(224, 85, 85, 0.6)',
                    borderColor: 'rgba(224, 85, 85, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

function backToSubjects() {
    document.getElementById('marksDetail').style.display = 'none';
    document.getElementById('subjectList').style.display = 'grid';
}
