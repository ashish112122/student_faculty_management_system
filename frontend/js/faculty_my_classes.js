const API_URL = 'http://localhost:5000/api';
let selectedClassId = null;
let selectedClassName = null;
let selectedAssessment = 'MST';
let currentView = 'selection';
let performanceChart = null;

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
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Classes data:', data);
        
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
        console.error('Error loading classes:', error);
        const grid = document.getElementById('class-grid');
        grid.innerHTML = '<p class="error-message">Failed to load classes. Error: ' + error.message + '</p>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function selectClass(classId, className) {
    selectedClassId = classId;
    selectedClassName = className;
    currentView = 'details';
    
    document.getElementById('class-title').textContent = className;
    document.getElementById('class-selection').style.display = 'none';
    document.getElementById('class-details').style.display = 'block';
    
    await loadClassData();
}

async function selectAssessment(assessment) {
    selectedAssessment = assessment;
    
    // Update button states
    document.querySelectorAll('.assessment-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    await loadClassData();
}

async function loadClassData() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/students?subject_id=${selectedClassId}&exam_type=${selectedAssessment}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        
        if (!data.students || data.students.length === 0) {
            showNoData();
            return;
        }
        
        const studentsWithMarks = data.students.filter(s => s.marks_obtained > 0);
        
        if (studentsWithMarks.length === 0) {
            showNoData();
            return;
        }
        
        hideNoData();
        renderStatistics(studentsWithMarks);
        renderChart(studentsWithMarks);
        renderTable(data.students);
    } catch (error) {
        console.error('Error loading class data:', error);
        showNoData();
    }
}

function renderStatistics(students) {
    const marks = students.map(s => s.marks_obtained);
    const avg = (marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(2);
    const highest = Math.max(...marks);
    const lowest = Math.min(...marks);
    
    document.getElementById('stat-avg').textContent = avg;
    document.getElementById('stat-high').textContent = highest;
    document.getElementById('stat-low').textContent = lowest;
    document.getElementById('stat-total').textContent = students.length;
}

function renderChart(students) {
    const canvas = document.getElementById('performance-chart');
    if (!canvas) return;
    
    if (performanceChart) {
        performanceChart.destroy();
    }
    
    const avg = students.reduce((sum, s) => sum + s.marks_obtained, 0) / students.length;
    
    performanceChart = new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels: students.map(s => s.student_name),
            datasets: [
                {
                    label: 'Marks',
                    data: students.map(s => s.marks_obtained),
                    backgroundColor: 'rgba(91, 106, 191, 0.8)',
                    borderColor: 'rgba(91, 106, 191, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Class Average',
                    data: students.map(() => avg),
                    type: 'line',
                    borderColor: '#e05555',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
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

function renderTable(students) {
    const tbody = document.getElementById('students-tbody');
    
    tbody.innerHTML = students.map((s, i) => {
        const grade = s.marks_obtained > 0 ? calculateGrade(s.marks_obtained) : '-';
        const marks = s.marks_obtained > 0 ? s.marks_obtained : 'Not entered';
        return `<tr>
            <td>${i + 1}</td>
            <td>${s.student_name}</td>
            <td>${s.branch}</td>
            <td>${s.semester}</td>
            <td>${marks}</td>
            <td>${grade !== '-' ? `<span class="badge grade-${grade}">${grade}</span>` : '-'}</td>
        </tr>`;
    }).join('');
}

function calculateGrade(marks) {
    if (marks >= 90) return 'A';
    if (marks >= 75) return 'B';
    if (marks >= 60) return 'C';
    if (marks >= 45) return 'D';
    return 'F';
}

function showNoData() {
    document.getElementById('no-data').style.display = 'block';
    document.getElementById('stats-section').style.display = 'none';
}

function hideNoData() {
    document.getElementById('no-data').style.display = 'none';
    document.getElementById('stats-section').style.display = 'block';
}

function goBack() {
    if (currentView === 'details') {
        currentView = 'selection';
        document.getElementById('class-details').style.display = 'none';
        document.getElementById('class-selection').style.display = 'block';
        if (performanceChart) {
            performanceChart.destroy();
            performanceChart = null;
        }
    } else {
        window.location.href = '/faculty';
    }
}
