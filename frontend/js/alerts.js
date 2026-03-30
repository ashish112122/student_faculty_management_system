const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }
    
    await loadAlerts();
});

async function loadAlerts() {
    const token = localStorage.getItem('token');
    
    try {
        const response = await fetch(`${API_URL}/student/alerts`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const alerts = await response.json();
        const alertsList = document.getElementById('alertsList');
        
        if (alerts.length === 0) {
            alertsList.innerHTML = '<p style="text-align:center; color:#666;">No alerts at this time</p>';
            return;
        }
        
        alerts.forEach(alert => {
            const card = document.createElement('div');
            card.className = `alert-card ${alert.alert_type.toLowerCase()}`;
            card.innerHTML = `
                <div class="alert-header">
                    <span class="alert-type">${alert.alert_type}</span>
                    <span class="alert-date">${alert.created_at}</span>
                </div>
                <div class="alert-message">${alert.message}</div>
            `;
            alertsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}
