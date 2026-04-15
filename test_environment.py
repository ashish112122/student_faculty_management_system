#!/usr/bin/env python3
"""
Test if the environment is ready to run the system
"""
import sys
import os
import socket

def test_port_available(port):
    """Check if a port is available"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def main():
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  🔍 ENVIRONMENT TEST                                      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    issues = []
    
    # Check Python version
    print(f"✓ Python version: {sys.version.split()[0]}")
    if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
        print("  ✓ Python 3.8+ requirement met")
    else:
        issues.append("Python 3.8+ is required")
    
    # Check venv
    venv_dir = os.path.join(os.path.dirname(__file__), 'venv')
    if os.path.exists(venv_dir):
        print(f"✓ Virtual environment exists at {venv_dir}")
    else:
        issues.append(f"Virtual environment not found at {venv_dir}")
    
    # Check directories
    dirs_to_check = ['backend', 'frontend', 'sql']
    for dir_name in dirs_to_check:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        if os.path.exists(dir_path):
            print(f"✓ {dir_name}/ directory exists")
        else:
            issues.append(f"{dir_name}/ directory not found")
    
    # Check ports
    print("\n🔍 Checking ports:")
    if test_port_available(5000):
        print("  ✓ Port 5000 is available (for backend)")
    else:
        issues.append("Port 5000 is already in use (backend)")
    
    if test_port_available(8000):
        print("  ✓ Port 8000 is available (for frontend)")
    else:
        print("  ⚠️  Port 8000 is already in use (check if frontend is running)")
    
    # Check key files
    print("\n🔍 Checking files:")
    files_to_check = {
        'backend/app.py': 'Backend server',
        'frontend/login_test.html': 'Login page',
        'start_frontend_server.py': 'Frontend starter'
    }
    
    for file_path, description in files_to_check.items():
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"  ✓ {description} ({file_path})")
        else:
            issues.append(f"{description} not found ({file_path})")
    
    # Summary
    print("\n" + "="*60)
    if not issues:
        print("✓ ALL CHECKS PASSED - System is ready to run!")
        print("\nTo start the system:")
        print("  1. Run: START_EVERYTHING.bat")
        print("     (this will start both backend and frontend)")
        print("\n  OR")
        print("\n  2. Run: START_FRONTEND_ONLY.bat")
        print("     (if backend is already running)")
        return 0
    else:
        print("❌ ISSUES FOUND:\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        return 1
    
if __name__ == "__main__":
    sys.exit(main())
