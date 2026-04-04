const API_URL = 'http://localhost:5000/api';
let selectedClassId = null;
let selectedClassName = null;
let currentView = 'selection';

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
    currentView = 'report';
    
    document.getElementById('report-title').textContent = `${className} - Marks Report`;
    document.getElementById('class-selection').style.display = 'none';
    document.getElementById('report-view').style.display = 'block';
    
    await loadReports();
}

async function loadReports() {
    const assessmentTypes = ['MST', 'EST', 'Assignment', 'Quiz'];
    const container = document.getElementById('reports-container');
    container.innerHTML = '';
    
    let hasData = false;
    
    for (const type of assessmentTypes) {
        const data = await loadAssessmentData(type);
        
        if (data && data.students && data.students.length > 0) {
            const studentsWithMarks = data.students.filter(s => s.marks_obtained > 0);
            
            if (studentsWithMarks.length > 0) {
                hasData = true;
                renderAssessmentReport(type, studentsWithMarks, container);
            }
        }
    }
    
    document.getElementById('no-data').style.display = hasData ? 'none' : 'block';
}

async function loadAssessmentData(assessmentType) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/students?subject_id=${selectedClassId}&exam_type=${assessmentType}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        console.error(`Error loading ${assessmentType}:`, error);
        return null;
    }
}

function renderAssessmentReport(type, students, container) {
    const marks = students.map(s => s.marks_obtained);
    const highest = Math.max(...marks);
    const lowest = Math.min(...marks);
    const average = (marks.reduce((a, b) => a + b, 0) / marks.length).toFixed(2);
    
    const section = document.createElement('div');
    section.className = 'report-section';
    section.innerHTML = `
        <h3>${type}</h3>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${highest}</div>
                <div class="stat-label">Highest</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${lowest}</div>
                <div class="stat-label">Lowest</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${average}</div>
                <div class="stat-label">Average</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${students.length}</div>
                <div class="stat-label">Students</div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="chart-${type}"></canvas>
        </div>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Student Name</th>
                        <th>Marks</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
                    ${students.map((s, i) => {
                        const grade = calculateGrade(s.marks_obtained);
                        return `<tr>
                            <td>${i + 1}</td>
                            <td>${s.student_name}</td>
                            <td>${s.marks_obtained}</td>
                            <td><span class="badge grade-${grade}">${grade}</span></td>
                        </tr>`;
                    }).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    container.appendChild(section);
    
    // Render chart
    setTimeout(() => renderChart(type, students), 100);
}

function renderChart(type, students) {
    const canvas = document.getElementById(`chart-${type}`);
    if (!canvas) return;
    
    const avg = students.reduce((sum, s) => sum + s.marks_obtained, 0) / students.length;
    
    new Chart(canvas.getContext('2d'), {
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

function calculateGrade(marks) {
    if (marks >= 90) return 'A';
    if (marks >= 75) return 'B';
    if (marks >= 60) return 'C';
    if (marks >= 45) return 'D';
    return 'F';
}

function goBack() {
    if (currentView === 'report') {
        currentView = 'selection';
        document.getElementById('report-view').style.display = 'none';
        document.getElementById('class-selection').style.display = 'block';
    } else {
        window.location.href = '/faculty';
    }
}
