import requests
import json

BASE_URL = 'http://localhost:5000'

def test_login():
    print("Testing login...")
    
    # Test student login
    response = requests.post(f'{BASE_URL}/api/login', json={
        'email': 'rohan.sharma@thapar.edu',
        'password': 'pass123'
    })
    
    print(f"Student login: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Token: {data.get('token')[:20]}...")
        print(f"  Name: {data.get('name')}")
        print(f"  Role: {data.get('role')}")
    
    # Test faculty login
    response = requests.post(f'{BASE_URL}/api/login', json={
        'email': 'dr.rajesh@thaparfac.edu',
        'password': 'pass123'
    })
    
    print(f"Faculty login: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Token: {data.get('token')[:20]}...")
        print(f"  Name: {data.get('name')}")
        print(f"  Role: {data.get('role')}")

if __name__ == '__main__':
    test_login()
