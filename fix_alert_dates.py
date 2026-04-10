"""
Fix alert dates to show varied creation times
"""
import sys
sys.path.insert(0, 'backend')
import oracledb
from config import Config
from datetime import datetime, timedelta

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def fix_alert_dates():
    print("=" * 80)
    print("FIXING ALERT DATES")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get all alerts
        cursor.execute("SELECT alert_id FROM alerts ORDER BY alert_id")
        alert_ids = [row[0] for row in cursor.fetchall()]
        
        print(f"\nFound {len(alert_ids)} alerts")
        print("Updating dates to spread over last 30 days...")
        
        # Update each alert with a varied date
        for idx, alert_id in enumerate(alert_ids):
            days_ago = idx % 30
            alert_date = datetime(2026, 4, 5) - timedelta(days=days_ago)
            
            cursor.execute("""
                UPDATE alerts 
                SET created_at = :created_at
                WHERE alert_id = :alert_id
            """, {'created_at': alert_date, 'alert_id': alert_id})
        
        conn.commit()
        
        print(f"✓ Updated {len(alert_ids)} alert dates")
        
        # Verify
        print("\nSample alert dates:")
        cursor.execute("""
            SELECT alert_id, TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI') as date_str
            FROM alerts
            WHERE ROWNUM <= 10
            ORDER BY created_at DESC
        """)
        
        for row in cursor.fetchall():
            print(f"  Alert {row[0]}: {row[1]}")
        
        print("\n" + "=" * 80)
        print("✓ ALERT DATES FIXED SUCCESSFULLY")
        print("=" * 80)
        print("\nAlerts now show varied dates from the last 30 days")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    fix_alert_dates()
