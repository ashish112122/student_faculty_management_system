import oracledb
from datetime import datetime, timedelta
from config import Config
from utils.email_service import send_alert_email

def get_db_connection():
    return oracledb.connect(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        dsn=Config.DB_DSN
    )

def check_attendance_alerts():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.student_id, s.user_id, u.email, u.name, sub.subject_id, sub.subject_name,
                   COUNT(CASE WHEN a.status = 'P' THEN 1 END) as present,
                   COUNT(*) as total
            FROM students s
            JOIN users u ON s.user_id = u.user_id
            JOIN student_subjects ss ON s.student_id = ss.student_id
            JOIN subjects sub ON ss.subject_id = sub.subject_id
            LEFT JOIN attendance a ON s.student_id = a.student_id AND sub.subject_id = a.subject_id
            GROUP BY s.student_id, s.user_id, u.email, u.name, sub.subject_id, sub.subject_name
        """)
        
        for row in cursor.fetchall():
            student_id, user_id, email, name, subject_id, subject_name, present, total = row
            
            if total == 0:
                continue
            
            percentage = (present / total) * 100
            
            alert_type = None
            message = None
            
            if percentage < 50:
                alert_type = 'Critical'
                message = f'Your attendance in {subject_name} is {percentage:.1f}% (below 50%). Critical situation.'
            elif percentage < 65:
                alert_type = 'Alert'
                message = f'Your attendance in {subject_name} is {percentage:.1f}% (below 65%). Immediate action required.'
            elif percentage < 75:
                alert_type = 'Warning'
                message = f'Your attendance in {subject_name} is {percentage:.1f}% (below 75%). Please improve.'
            
            if alert_type:
                cursor.execute("""
                    SELECT COUNT(*) FROM alerts
                    WHERE student_id = :sid AND alert_type = :atype
                    AND created_at > SYSDATE - 15
                """, {'sid': student_id, 'atype': alert_type})
                
                recent_alert = cursor.fetchone()[0]
                
                if recent_alert == 0:
                    cursor.execute("""
                        INSERT INTO alerts (alert_id, student_id, alert_type, message, created_at)
                        VALUES (alerts_seq.NEXTVAL, :sid, :atype, :msg, SYSDATE)
                    """, {'sid': student_id, 'atype': alert_type, 'msg': message})
                    
                    send_alert_email(email, name, alert_type, message)
        
        conn.commit()
        print(f"Alert check completed at {datetime.now()}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    check_attendance_alerts()
