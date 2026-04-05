"""
Test all API endpoints and verify database connections
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_home():
    print("\n1. Testing Home Endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")
    return response.status_code == 200

def test_student_login():
    print("\n2. Testing Student Login...")
    data = {
        "email": "rohan.sharma.2q34.3@thapar.edu",
        "password": "pass123"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Name: {result.get('name')}")
        print(f"   Role: {result.get('role')}")
        print(f"   Token: {result.get('token')[:50]}...")
        return result.get('token')
    else:
        print(f"   Error: {response.text}")
        return None

def test_faculty_login():
    print("\n3. Testing Faculty Login...")
    data = {
        "email": "dr.rajesh@thaparfac.edu",
        "password": "pass123"
    }
    response = requests.post(f"{BASE_URL}/api/login", json=data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Name: {result.get('name')}")
        print(f"   Role: {result.get('role')}")
        print(f"   Token: {result.get('token')[:50]}...")
        return result.get('token')
    else:
        print(f"   Error: {response.text}")
        return None

def test_student_dashboard(token):
    print("\n4. Testing Student Dashboard...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/student/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Student: {result.get('name')}")
        print(f"   Batch: {result.get('class_name')}")
        print(f"   Semester: {result.get('semester')}")
        print(f"   CGPA: {result.get('cgpa')}")
        print(f"   Subjects: {len(result.get('subjects', []))}")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_student_marks(token, subject_id):
    print(f"\n5. Testing Student Marks (Subject {subject_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/student/marks/{subject_id}", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        marks = result.get('marks', {})
        class_avg = result.get('class_average', {})
        print(f"   MST: {marks.get('MST', {}).get('obtained', 0)}/{marks.get('MST', {}).get('max', 0)} (Avg: {class_avg.get('MST', 0)})")
        print(f"   EST: {marks.get('EST', {}).get('obtained', 0)}/{marks.get('EST', {}).get('max', 0)} (Avg: {class_avg.get('EST', 0)})")
        print(f"   Quiz: {marks.get('Quiz', {}).get('obtained', 0)}/{marks.get('Quiz', {}).get('max', 0)} (Avg: {class_avg.get('Quiz', 0)})")
        print(f"   Assignment: {marks.get('Assignment', {}).get('obtained', 0)}/{marks.get('Assignment', {}).get('max', 0)} (Avg: {class_avg.get('Assignment', 0)})")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_student_attendance(token, subject_id):
    print(f"\n6. Testing Student Attendance (Subject {subject_id})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/student/attendance/{subject_id}", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Total Classes: {result.get('total', 0)}")
        print(f"   Present: {result.get('present', 0)}")
        print(f"   Percentage: {result.get('percentage', 0)}%")
        print(f"   Records: {len(result.get('records', []))} days")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_student_alerts(token):
    print("\n7. Testing Student Alerts...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/student/alerts", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Total Alerts: {len(result)}")
        for alert in result[:3]:
            print(f"   - {alert.get('type')}: {alert.get('message')} (Read: {alert.get('is_read')})")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_student_feedback_subjects(token):
    print("\n8. Testing Student Feedback Subjects...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/student/feedback/subjects", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Subjects: {len(result)}")
        for subj in result[:3]:
            print(f"   - {subj.get('subject_name')} (Faculty: {subj.get('faculty_name')})")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_faculty_dashboard(token):
    print("\n9. Testing Faculty Dashboard...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/faculty/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Faculty: {result.get('name')}")
        print(f"   Department: {result.get('department')}")
        print(f"   Subjects: {len(result.get('subjects', []))}")
        for subj in result.get('subjects', [])[:3]:
            print(f"   - {subj.get('subject_name')} ({subj.get('class_name')})")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_faculty_marks(token, subject_id, class_name):
    print(f"\n10. Testing Faculty Marks (Subject {subject_id}, Class {class_name})...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/faculty/marks/{subject_id}/{class_name}", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Students: {len(result)}")
        for student in result[:3]:
            print(f"   - {student.get('name')}: MST={student.get('mid')}, EST={student.get('final')}, Total={student.get('total')}")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def test_faculty_feedback_threads(token):
    print("\n11. Testing Faculty Feedback Threads...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/faculty/feedback/threads", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Threads: {len(result)}")
        return result
    else:
        print(f"   Error: {response.text}")
        return None

def main():
    print("=" * 80)
    print("TESTING ALL API ENDPOINTS")
    print("=" * 80)
    
    # Test home
    if not test_home():
        print("\n❌ Backend not responding!")
        return
    
    # Test student login and APIs
    student_token = test_student_login()
    if student_token:
        student_data = test_student_dashboard(student_token)
        if student_data and student_data.get('subjects'):
            subject_id = student_data['subjects'][0]['subject_id']
            test_student_marks(student_token, subject_id)
            test_student_attendance(student_token, subject_id)
        test_student_alerts(student_token)
        test_student_feedback_subjects(student_token)
    
    # Test faculty login and APIs
    faculty_token = test_faculty_login()
    if faculty_token:
        faculty_data = test_faculty_dashboard(faculty_token)
        if faculty_data and faculty_data.get('subjects'):
            subject = faculty_data['subjects'][0]
            test_faculty_marks(faculty_token, subject['subject_id'], subject['class_name'])
        test_faculty_feedback_threads(faculty_token)
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED!")
    print("=" * 80)
    print("\nCredentials for testing:")
    print("  Student: rohan.sharma.2q34.3@thapar.edu / pass123")
    print("  Faculty: dr.rajesh@thaparfac.edu / pass123")
    print("\nBackend URL: http://localhost:5000")

if __name__ == '__main__':
    main()
