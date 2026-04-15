#!/usr/bin/env python3
"""
Start a simple HTTP server for the frontend
"""
import os
import sys
import http.server
import socketserver
import webbrowser
import threading
import time

PORT = 8000
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        return super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[Frontend Server] {format % args}")

def open_browser():
    """Open the login page in the default browser after server starts"""
    time.sleep(1.5)  # Give server time to start
    url = f'http://localhost:{PORT}/login_test.html'
    print(f"\n✓ Frontend server started successfully!")
    print(f"✓ Opening login page: {url}\n")
    webbrowser.open(url)

try:
    os.chdir(FRONTEND_DIR)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"╔════════════════════════════════════════════════════════════╗")
        print(f"║  🚀 FRONTEND SERVER RUNNING                               ║")
        print(f"║  📍 URL: http://localhost:{PORT}                         ║")
        print(f"║  📂 Serving: {FRONTEND_DIR}                             ║")
        print(f"║  ⏹️  Press Ctrl+C to stop                                 ║")
        print(f"╚════════════════════════════════════════════════════════════╝\n")
        
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n✓ Frontend server stopped")
    sys.exit(0)
except OSError as e:
    print(f"\n❌ Error: {e}")
    if "Address already in use" in str(e):
        print(f"   Port {PORT} is already in use. Try closing any running frontend servers.")
    sys.exit(1)
