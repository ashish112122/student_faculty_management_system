"""
Test CORS Configuration
Run this to verify CORS is working
"""

import requests
import json

def test_cors():
    print("="*50)
    print("Testing CORS Configuration")
    print("="*50)
    print()
    
    backend_url = "http://localhost:5000/api/login"
    frontend_origin = "http://localhost:8000"
    
    print(f"Backend URL: {backend_url}")
    print(f"Frontend Origin: {frontend_origin}")
    print()
    
    # Test 1: OPTIONS request (preflight)
    print("Test 1: OPTIONS Request (Preflight)")
    print("-" * 50)
    
    try:
        response = requests.options(
            backend_url,
            headers={
                'Origin': frontend_origin,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"CORS Headers:")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        for header, value in cors_headers.items():
            if value:
                print(f"  ✓ {header}: {value}")
            else:
                print(f"  ❌ {header}: NOT FOUND")
        
        if all(cors_headers.values()):
            print("\n✅ CORS preflight is working!")
        else:
            print("\n❌ CORS preflight is NOT working!")
            print("\nSOLUTION: Restart backend server")
            print("  1. Stop backend (Ctrl+C)")
            print("  2. cd backend")
            print("  3. python app.py")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("\nSOLUTION: Start the backend server")
        print("  cd backend")
        print("  python app.py")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print()
    
    # Test 2: POST request (actual login)
    print("Test 2: POST Request (Login)")
    print("-" * 50)
    
    try:
        response = requests.post(
            backend_url,
            headers={
                'Origin': frontend_origin,
                'Content-Type': 'application/json'
            },
            json={
                'email': 'rohan.sharma@thapar.edu',
                'password': 'password123'
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            print(f"  Token received: {data.get('token')[:20]}...")
            print(f"  User: {data.get('name')}")
            print(f"  Role: {data.get('role')}")
        elif response.status_code == 401:
            print("⚠️ Invalid credentials (but CORS is working!)")
            print("  This means backend is responding correctly")
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            print(f"  Response: {response.text}")
        
        # Check CORS headers in response
        origin_header = response.headers.get('Access-Control-Allow-Origin')
        if origin_header:
            print(f"\n✅ CORS header in response: {origin_header}")
        else:
            print("\n❌ No CORS header in response")
            print("  Backend needs to be restarted")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("="*50)
    print("Test Complete")
    print("="*50)
    print()
    
    print("If tests passed:")
    print("  ✓ Backend is running")
    print("  ✓ CORS is configured")
    print("  ✓ Login should work in browser")
    print()
    print("If tests failed:")
    print("  1. Make sure backend is running: python app.py")
    print("  2. Restart backend if it was already running")
    print("  3. Clear browser cache")
    print("  4. Try Incognito mode")

if __name__ == '__main__':
    test_cors()
    input("\nPress Enter to exit...")
