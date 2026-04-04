const API_URL = 'http://localhost:5000/api';
let currentStep = 1;
let selectedClassId = null;
let selectedClassName = null;
let selectedStudentId = null;
let selectedStudentName = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }
    
    loadClasses();
    document.getElementById('marks-form').addEventListener('submit', handleSubmitMarks);
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
        console.log('Faculty dashboard data:', data);
        
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
    currentStep = 2;
    
    document.getElementById('selected-class-name').textContent = className;
    document.getElementById('step-class').style.display = 'none';
    document.getElementById('step-student').style.display = 'block';
    
    await loadStudents(classId);
}

async function loadStudents(classId) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/faculty/students?subject_id=${classId}&exam_type=MST`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Students data:', data);
        
        const list = document.getElementById('student-list');
        
        if (!data.students || data.students.length === 0) {
            list.innerHTML = '<p class="empty-message">No students enrolled</p>';
            return;
        }
        
        list.innerHTML = data.students.map(student => `
            <div class="list-item" onclick="selectStudent(${student.student_id}, '${escapeHtml(student.student_name)}')">
                <div>
                    <div class="item-title">${escapeHtml(student.student_name)}</div>
                    <div class="item-subtitle">ID: ${student.student_id} | ${student.branch} | Sem ${student.semester}</div>
                </div>
                <div class="arrow">→</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading students:', error);
        document.getElementById('student-list').innerHTML = '<p class="error-message">Failed to load students. Error: ' + error.message + '</p>';
    }
}

function selectStudent(studentId, studentName) {
    selectedStudentId = studentId;
    selectedStudentName = studentName;
    currentStep = 3;
    
    document.getElementById('selected-student-name').textContent = studentName;
    document.getElementById('marks-class-name').textContent = selectedClassName;
    document.getElementById('step-student').style.display = 'none';
    document.getElementById('step-marks').style.display = 'block';
    
    // Reset form
    document.getElementById('marks-form').reset();
    hideMessage();
}

async function handleSubmitMarks(e) {
    e.preventDefault();
    
    const token = localStorage.getItem('token');
    const assessmentType = document.getElementById('assessment-type').value;
    const marksObtained = parseFloat(document.getElementById('marks-obtained').value);
    const maxMarks = parseFloat(document.getElementById('max-marks').value);
    
    if (marksObtained > maxMarks) {
        showMessage('Marks obtained cannot exceed maximum marks', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/faculty/marks/add`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: selectedStudentId,
                subject_id: selectedClassId,
                assessment_type: assessmentType,
                marks_obtained: marksObtained,
                max_marks: maxMarks
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(`${data.message}! Grade: ${data.grade}`, 'success');
            setTimeout(() => {
                document.getElementById('marks-form').reset();
                hideMessage();
            }, 2000);
        } else {
            showMessage(data.message || 'Failed to save marks', 'error');
        }
    } catch (error) {
        console.error('Error saving marks:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    msg.style.display = 'block';
}

function hideMessage() {
    document.getElementById('message').style.display = 'none';
}

function goBack() {
    if (currentStep === 3) {
        // From marks form back to student list
        currentStep = 2;
        document.getElementById('step-marks').style.display = 'none';
        document.getElementById('step-student').style.display = 'block';
    } else if (currentStep === 2) {
        // From student list back to class selection
        currentStep = 1;
        document.getElementById('step-student').style.display = 'none';
        document.getElementById('step-class').style.display = 'block';
    } else {
        // From class selection back to dashboard
        window.location.href = '/faculty';
    }
}
