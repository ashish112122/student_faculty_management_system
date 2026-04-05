import requests
import json

BASE_URL = "http://localhost:5000"

def test_login():
    """Test login with faculty user"""
    print("=" * 50)
    print("Testing Faculty Login")
    print("=" * 50)
    
    payload = {
        "email": "faculty1@univ.edu",
        "password": "pass123",
        "role": "faculty"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            token = data.get('token')
            print(f"\n✓ Login successful! Token: {token[:20]}...")
            return token
        else:
            print(f"✗ Login failed: {data}")
            return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def test_faculty_info(token):
    """Test fetching faculty information"""
    print("\n" + "=" * 50)
    print("Testing Faculty Info Endpoint")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/faculty/info", headers=headers)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✓ Faculty info retrieved successfully!")
        else:
            print(f"✗ Failed to retrieve faculty info")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_faculty_subjects(token):
    """Test fetching faculty subjects"""
    print("\n" + "=" * 50)
    print("Testing Faculty Subjects Endpoint")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/faculty/subjects", headers=headers)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✓ Faculty subjects retrieved successfully!")
        else:
            print(f"✗ Failed to retrieve faculty subjects")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_student_login():
    """Test login with student user"""
    print("\n" + "=" * 50)
    print("Testing Student Login")
    print("=" * 50)
    
    payload = {
        "email": "student1@univ.edu",
        "password": "pass123",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            token = data.get('token')
            print(f"\n✓ Student login successful! Token: {token[:20]}...")
            return token
        else:
            print(f"✗ Student login failed: {data}")
            return None
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None

def test_student_info(token):
    """Test fetching student information"""
    print("\n" + "=" * 50)
    print("Testing Student Info Endpoint")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/student/info", headers=headers)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✓ Student info retrieved successfully!")
        else:
            print(f"✗ Failed to retrieve student info")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def test_student_subjects(token):
    """Test fetching student subjects"""
    print("\n" + "=" * 50)
    print("Testing Student Subjects Endpoint")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/student/subjects", headers=headers)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        if response.status_code == 200:
            print("✓ Student subjects retrieved successfully!")
        else:
            print(f"✗ Failed to retrieve student subjects")
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("STUDENT-FACULTY MANAGEMENT SYSTEM - API TESTS")
    print("=" * 50)
    
    # Test faculty flow
    faculty_token = test_login()
    if faculty_token:
        test_faculty_info(faculty_token)
        test_faculty_subjects(faculty_token)
    
    # Test student flow
    student_token = test_student_login()
    if student_token:
        test_student_info(student_token)
        test_student_subjects(student_token)
    
    print("\n" + "=" * 50)
    print("TESTS COMPLETE")
    print("=" * 50)
