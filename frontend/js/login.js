document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    console.log('Login form submitted');
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('error-message');
    
    console.log('Email:', email);
    console.log('Attempting login...');
    
    // Clear previous errors
    errorDiv.textContent = '';
    errorDiv.classList.remove('show');
    
    try {
        console.log('Sending request to backend...');
        
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok) {
            console.log('Login successful!');
            localStorage.setItem('token', data.token);
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('role', data.role);
            
            if (data.role === 'student') {
                console.log('Redirecting to dashboard...');
                window.location.href = 'dashboard.html';
            } else if (data.role === 'faculty') {
                console.log('Redirecting to faculty dashboard...');
                window.location.href = 'faculty-dashboard.html';
            }
        } else {
            console.log('Login failed:', data.message);
            errorDiv.textContent = data.message;
            errorDiv.classList.add('show');
        }
    } catch (error) {
        console.error('Login error:', error);
        errorDiv.textContent = 'Connection error. Please try again. Make sure backend is running.';
        errorDiv.classList.add('show');
    }
});
