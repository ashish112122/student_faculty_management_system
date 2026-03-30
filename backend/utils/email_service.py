import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def send_alert_email(student_email, student_name, alert_type, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_CONFIG['sender_email']
        msg['To'] = student_email
        msg['Subject'] = f'Attendance {alert_type} - Action Required'
        
        body = f"""
        Dear {student_name},
        
        {message}
        
        Please take necessary action to improve your attendance.
        
        Regards,
        University Administration
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(Config.EMAIL_CONFIG['smtp_server'], Config.EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(Config.EMAIL_CONFIG['sender_email'], Config.EMAIL_CONFIG['sender_password'])
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
