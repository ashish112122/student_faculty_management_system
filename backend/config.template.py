"""
Configuration Template
Copy this file to config.py and update with your credentials
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Oracle Database Configuration
    # Update these with your Oracle credentials
    DB_USER = os.environ.get('DB_USER') or 'system'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'YOUR_ORACLE_PASSWORD_HERE'
    DB_DSN = os.environ.get('DB_DSN') or 'localhost:1521/XE'
    
    # Alert System Configuration
    ALERT_CHECK_INTERVAL = 15  # days
    
    # Email Configuration (Optional - for alert notifications)
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'your-email@example.com',
        'sender_password': 'your-email-password'
    }
