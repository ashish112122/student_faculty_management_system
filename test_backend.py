import requests
import json

# Test if backend is running
try:
    response = requests.get('http://localhost:5000/')
    print(f"Root endpoint: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error connecting to root: {e}")

# Test login endpoint
try:
    response = requests.post('http://localhost:5000/api/login', 
                            json={'email': 'test@test.com', 'password': 'test'},
                            headers={'Content-Type': 'application/json'})
    print(f"Login endpoint: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error connecting to login: {e}")
