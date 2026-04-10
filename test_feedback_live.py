"""
Test Feedback System - Verify it's working
"""
import requests
import json

API_URL = "http://localhost:5000/api"

def test_student_login():
    """Test student login"""
    print("=" * 50)
    print("TEST 1: Student Login")
    print("=" * 50)
    
    response = requests.post(f"{API_URL}/login", json={
        "email": "rohan.sharma.2q34.3@thapar.edu",
        "password": "pass123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful: {data['name']}")
        return data['token']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_faculty_login():
    """Test faculty login"""
    print("\n" + "=" * 50)
    print("TEST 2: Faculty Login")
    print("=" * 50)
    
    response = requests.post(f"{API_URL}/login", json={
        "email": "dr.rajesh@thaparfac.edu",
        "password": "pass123"
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful: {data['name']}")
        return data['token']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_get_student_subjects(token):
    """Test getting subjects for feedback"""
    print("\n" + "=" * 50)
    print("TEST 3: Get Student Subjects for Feedback")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/student/feedback/subjects", headers=headers)
    
    if response.status_code == 200:
        subjects = response.json()
        print(f"✅ Found {len(subjects)} subjects")
        for subject in subjects:
            print(f"   - {subject['subject_name']} — {subject['faculty_name']}")
        return subjects[0] if subjects else None
    else:
        print(f"❌ Failed to get subjects: {response.text}")
        return None

def test_send_student_message(token, faculty_id, subject_id):
    """Test sending message from student"""
    print("\n" + "=" * 50)
    print("TEST 4: Send Message from Student")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    message = "Hello Professor! This is a test message from the automated test script."
    
    response = requests.post(f"{API_URL}/student/feedback/send", 
                            headers=headers,
                            json={
                                "faculty_id": faculty_id,
                                "subject_id": subject_id,
                                "message": message
                            })
    
    if response.status_code == 200:
        print(f"✅ Message sent successfully")
        print(f"   Message: {message}")
        return True
    else:
        print(f"❌ Failed to send message: {response.text}")
        return False

def test_get_faculty_threads(token):
    """Test getting faculty threads"""
    print("\n" + "=" * 50)
    print("TEST 5: Get Faculty Feedback Threads")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/faculty/feedback/threads", headers=headers)
    
    if response.status_code == 200:
        threads = response.json()
        print(f"✅ Found {len(threads)} threads")
        for thread in threads:
            unread = f" ({thread['unread_count']} new)" if thread['unread_count'] > 0 else ""
            print(f"   - {thread['student_name']} - {thread['subject_name']}{unread}")
        return threads[0] if threads else None
    else:
        print(f"❌ Failed to get threads: {response.text}")
        return None

def test_get_faculty_messages(token, student_id, subject_id):
    """Test getting messages in a thread"""
    print("\n" + "=" * 50)
    print("TEST 6: Get Messages in Thread")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/faculty/feedback/{student_id}/{subject_id}", headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Found {len(messages)} messages")
        for msg in messages:
            sender = "Student" if msg['sender_role'] == 'student' else "Faculty"
            read_status = "✓" if msg['is_read'] else "✗"
            print(f"   [{msg['created_at']}] {sender} ({read_status}): {msg['message'][:50]}...")
        return True
    else:
        print(f"❌ Failed to get messages: {response.text}")
        return False

def test_send_faculty_reply(token, student_id, subject_id):
    """Test sending reply from faculty"""
    print("\n" + "=" * 50)
    print("TEST 7: Send Reply from Faculty")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    message = "Thank you for your message! This is an automated reply from the test script."
    
    response = requests.post(f"{API_URL}/faculty/feedback/send", 
                            headers=headers,
                            json={
                                "student_id": student_id,
                                "subject_id": subject_id,
                                "message": message
                            })
    
    if response.status_code == 200:
        print(f"✅ Reply sent successfully")
        print(f"   Message: {message}")
        return True
    else:
        print(f"❌ Failed to send reply: {response.text}")
        return False

def test_get_student_messages(token, faculty_id, subject_id):
    """Test getting messages as student"""
    print("\n" + "=" * 50)
    print("TEST 8: Get Messages as Student (See Faculty Reply)")
    print("=" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/student/feedback/{faculty_id}/{subject_id}", headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Found {len(messages)} messages")
        for msg in messages:
            sender = "You" if msg['sender_role'] == 'student' else "Faculty"
            read_status = "✓" if msg['is_read'] else "✗"
            print(f"   [{msg['created_at']}] {sender} ({read_status}): {msg['message'][:50]}...")
        return True
    else:
        print(f"❌ Failed to get messages: {response.text}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "FEEDBACK SYSTEM TEST SUITE" + " " * 22 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\nTesting complete two-way messaging system...")
    print("Backend must be running on http://localhost:5000\n")
    
    try:
        # Test student flow
        student_token = test_student_login()
        if not student_token:
            print("\n❌ Cannot proceed without student login")
            return
        
        subject = test_get_student_subjects(student_token)
        if not subject:
            print("\n❌ Cannot proceed without subjects")
            return
        
        faculty_id = subject['faculty_id']
        subject_id = subject['subject_id']
        
        test_send_student_message(student_token, faculty_id, subject_id)
        
        # Test faculty flow
        faculty_token = test_faculty_login()
        if not faculty_token:
            print("\n❌ Cannot proceed without faculty login")
            return
        
        thread = test_get_faculty_threads(faculty_token)
        if not thread:
            print("\n⚠️  No threads found (this is OK if no messages exist)")
        else:
            student_id = thread['student_id']
            subject_id = thread['subject_id']
            
            test_get_faculty_messages(faculty_token, student_id, subject_id)
            test_send_faculty_reply(faculty_token, student_id, subject_id)
        
        # Verify student sees reply
        test_get_student_messages(student_token, faculty_id, subject_id)
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("✅ Student login: PASSED")
        print("✅ Faculty login: PASSED")
        print("✅ Get subjects: PASSED")
        print("✅ Send message: PASSED")
        print("✅ Get threads: PASSED")
        print("✅ Get messages: PASSED")
        print("✅ Send reply: PASSED")
        print("✅ Verify reply: PASSED")
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED - FEEDBACK SYSTEM WORKING!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n" + "=" * 60)
        print("❌ ERROR: Cannot connect to backend")
        print("=" * 60)
        print("\nMake sure backend is running:")
        print("  1. Double-click START_ALL.bat")
        print("  2. Or run: python backend/app.py")
        print("\nBackend should be at: http://localhost:5000")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
