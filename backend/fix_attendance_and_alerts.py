"""
Fix attendance date range (1 Jan - 1 April) and alert timestamps
"""
import oracledb
from config import Config
from datetime import datetime, timedelta
import random

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def fix_attendance_and_alerts():
    print("=" * 60)
    print("FIXING ATTENDANCE DATE RANGE AND ALERT TIMESTAMPS")
    print("=" * 60)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. Delete attendance records after April 1, 2026
        print("\n1. Removing attendance records after April 1, 2026...")
        cursor.execute("""
            DELETE FROM attendance 
            WHERE attendance_date > TO_DATE('2026-04-01', 'YYYY-MM-DD')
        """)
        deleted_count = cursor.rowcount
        conn.commit()
        print(f"   ✓ Deleted {deleted_count} attendance records after April 1")
        
        # 2. Delete all existing alerts
        print("\n2. Deleting old alerts...")
        cursor.execute("DELETE FROM alerts")
        deleted_alerts = cursor.rowcount
        conn.commit()
        print(f"   ✓ Deleted {deleted_alerts} old alerts")
        
        # 3. Regenerate alerts with proper timestamps
        print("\n3. Generating new alerts with proper timestamps...")
        
        cursor.execute("""
            SELECT s.student_id, a.subject_id, sub.subject_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
            FROM students s
            JOIN attendance a ON s.student_id = a.student_id
            JOIN subjects sub ON a.subject_id = sub.subject_id
            GROUP BY s.student_id, a.subject_id, sub.subject_name
            HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
        """)
        
        alert_results = cursor.fetchall()
        alert_count = 0
        
        for idx, (student_id, subject_id, subject_name, total, present) in enumerate(alert_results):
            percentage = round((present / total) * 100, 2)
            alert_type = 'Critical' if percentage < 50 else 'Warning'
            message = f"Low attendance in {subject_name}: {percentage}%"
            
            # Vary the alert creation date and time (spread over last 30 days)
            days_ago = idx % 30
            hours = random.randint(8, 18)  # Between 8 AM and 6 PM
            minutes = random.randint(0, 59)
            alert_date = datetime(2026, 4, 5, hours, minutes) - timedelta(days=days_ago)
            
            cursor.execute("""
                INSERT INTO alerts (alert_id, student_id, subject_id, alert_type, message, is_read, created_at)
                VALUES (alerts_seq.NEXTVAL, :student_id, :subject_id, :alert_type, :message, 0, :created_at)
            """, {
                'student_id': student_id,
                'subject_id': subject_id,
                'alert_type': alert_type,
                'message': message,
                'created_at': alert_date
            })
            alert_count += 1
        
        conn.commit()
        print(f"   ✓ Generated {alert_count} alerts with proper timestamps")
        
        # 4. Verify changes
        print("\n4. Verifying changes...")
        
        # Check attendance date range
        cursor.execute("""
            SELECT MIN(attendance_date), MAX(attendance_date), COUNT(*)
            FROM attendance
        """)
        min_date, max_date, total_attendance = cursor.fetchone()
        print(f"   ✓ Attendance range: {min_date.strftime('%d %b %Y')} to {max_date.strftime('%d %b %Y')}")
        print(f"   ✓ Total attendance records: {total_attendance}")
        
        # Check alert timestamps
        cursor.execute("""
            SELECT COUNT(*), MIN(created_at), MAX(created_at)
            FROM alerts
        """)
        alert_count, min_alert, max_alert = cursor.fetchone()
        print(f"   ✓ Total alerts: {alert_count}")
        print(f"   ✓ Alert date range: {min_alert.strftime('%d %b %Y %I:%M %p')} to {max_alert.strftime('%d %b %Y %I:%M %p')}")
        
        # Sample some alerts to show varied timestamps
        cursor.execute("""
            SELECT alert_type, message, created_at
            FROM alerts
            WHERE ROWNUM <= 5
            ORDER BY created_at DESC
        """)
        print("\n   Sample alerts with timestamps:")
        for alert_type, message, created_at in cursor.fetchall():
            print(f"   - [{alert_type}] {message}")
            print(f"     Time: {created_at.strftime('%d %b %Y — %I:%M %p')}")
        
        print("\n" + "=" * 60)
        print("✅ ALL FIXES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nChanges made:")
        print("1. ✅ Attendance date range: 1 Jan - 1 April 2026")
        print("2. ✅ Alerts have proper timestamps (not 00:00)")
        print("3. ✅ Alert times vary between 8 AM - 6 PM")
        print("\nNext steps:")
        print("- Restart backend server to apply changes")
        print("- Test on both student and faculty portals")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    fix_attendance_and_alerts()
