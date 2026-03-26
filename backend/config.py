import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    DB_USER = os.environ.get('DB_USER') or 'system'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'Vanshi@Oracle1'
    DB_DSN = os.environ.get('DB_DSN') or 'localhost:1521/XE'
    
    ALERT_CHECK_INTERVAL = 15
    
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'sender_email': 'alerts@university.edu',
        'sender_password': 'your-email-password'
    }