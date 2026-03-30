const API_URL = 'http://localhost:5000/api';
let currentSubjectId = null;

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
        subjectList.innerHTML = '';
        
        subjects.forEach(subject => {
            const card = document.createElement('div');
            card.className = 'subject-card';
            card.innerHTML = `<h3>${subject.subject_name}</h3><p class="subject-code">${subject.subject_code || ''}</p>`;
            card.onclick = () => openConversation(subject.subject_id, subject.subject_name);
            subjectList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading subjects:', error);
    }
}

async function openConversation(subjectId, subjectName) {
    currentSubjectId = subjectId;
    
    document.getElementById('subjectList').style.display = 'none';
    document.getElementById('conversationView').style.display = 'flex';
    document.getElementById('subjectName').textContent = subjectName;
    
    await loadMessages(subjectId);
}

async function loadMessages(subjectId) {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/feedback?subject_id=${subjectId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const messages = await response.json();
        const thread = document.getElementById('messageThread');
        thread.innerHTML = '';
        
        if (messages.length === 0) {
            thread.innerHTML = '<div style="text-align: center; padding: 40px; color: #999;">No messages yet. Start a conversation!</div>';
        } else {
            messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${msg.sender_role}`;
                messageDiv.innerHTML = `
                    <div class="message-header">
                        <span>${msg.sender_name}</span>
                        <span>${msg.created_at}</span>
                    </div>
                    <div class="message-text">${msg.message}</div>
                `;
                thread.appendChild(messageDiv);
            });
        }
        
        thread.scrollTop = thread.scrollHeight;
    } catch (error) {
        console.error('Error loading messages:', error);
    }
}

async function sendMessage() {
    const token = localStorage.getItem('token');
    const messageText = document.getElementById('messageText').value.trim();
    
    if (!messageText) return;
    
    try {
        await fetch(`${API_URL}/student/feedback`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                subject_id: currentSubjectId,
                message: messageText
            })
        });
        
        document.getElementById('messageText').value = '';
        await loadMessages(currentSubjectId);
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function backToSubjectList() {
    document.getElementById('conversationView').style.display = 'none';
    document.getElementById('subjectList').style.display = 'grid';
    currentSubjectId = null;
}
