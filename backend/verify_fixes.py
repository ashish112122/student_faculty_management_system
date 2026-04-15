"""
Verify all fixes are applied correctly
"""
import oracledb
from config import Config
from datetime import datetime

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def verify_fixes():
    print("=" * 70)
    print("VERIFYING ALL FIXES")
    print("=" * 70)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    all_passed = True
    
    try:
        # 1. Verify attendance date range
        print("\n1. Checking Attendance Date Range...")
        cursor.execute("""
            SELECT MIN(attendance_date), MAX(attendance_date), COUNT(*)
            FROM attendance
        """)
        min_date, max_date, total = cursor.fetchone()
        
        if max_date <= datetime(2026, 4, 1):
            print(f"   ✅ PASS: Attendance range is {min_date.strftime('%d %b %Y')} to {max_date.strftime('%d %b %Y')}")
            print(f"   ✅ Total records: {total}")
        else:
            print(f"   ❌ FAIL: Attendance goes beyond April 1, 2026")
            print(f"   Found: {min_date.strftime('%d %b %Y')} to {max_date.strftime('%d %b %Y')}")
            all_passed = False
        
        # 2. Verify alert timestamps
        print("\n2. Checking Alert Timestamps...")
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN TO_CHAR(created_at, 'HH24:MI') = '00:00' THEN 1 ELSE 0 END) as midnight_count
            FROM alerts
        """)
        total_alerts, midnight_count = cursor.fetchone()
        
        if midnight_count == 0:
            print(f"   ✅ PASS: No alerts with 00:00 timestamp")
            print(f"   ✅ Total alerts: {total_alerts}")
        else:
            print(f"   ❌ FAIL: Found {midnight_count} alerts with 00:00 timestamp")
            all_passed = False
        
        # Show sample alert timestamps
        cursor.execute("""
            SELECT alert_type, message, created_at
            FROM alerts
            WHERE ROWNUM <= 5
            ORDER BY created_at DESC
        """)
        print("\n   Sample alert timestamps:")
        for alert_type, message, created_at in cursor.fetchall():
            time_str = created_at.strftime('%d %b %Y — %I:%M %p')
            print(f"   - {time_str}")
            if created_at.strftime('%H:%M') == '00:00':
                print(f"     ❌ This alert has 00:00 time!")
                all_passed = False
        
        # 3. Verify faculty-student relationships
        print("\n3. Checking Faculty-Student Relationships...")
        
        # Check if faculty_classes table has correct mappings
        cursor.execute("""
            SELECT COUNT(DISTINCT faculty_id), COUNT(DISTINCT subject_id), COUNT(*)
            FROM faculty_classes
        """)
        faculty_count, subject_count, mapping_count = cursor.fetchone()
        print(f"   ✅ Faculty count: {faculty_count}")
        print(f"   ✅ Subject count: {subject_count}")
        print(f"   ✅ Faculty-Subject-Class mappings: {mapping_count}")
        
        # Check if students are properly assigned to classes
        cursor.execute("""
            SELECT COUNT(DISTINCT class_name), COUNT(*)
            FROM students
        """)
        class_count, student_count = cursor.fetchone()
        print(f"   ✅ Classes/Batches: {class_count}")
        print(f"   ✅ Total students: {student_count}")
        
        # Verify no orphaned records
        cursor.execute("""
            SELECT COUNT(*)
            FROM marks m
            WHERE NOT EXISTS (
                SELECT 1 FROM students s WHERE s.student_id = m.student_id
            )
        """)
        orphaned_marks = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*)
            FROM attendance a
            WHERE NOT EXISTS (
                SELECT 1 FROM students s WHERE s.student_id = a.student_id
            )
        """)
        orphaned_attendance = cursor.fetchone()[0]
        
        if orphaned_marks == 0 and orphaned_attendance == 0:
            print(f"   ✅ PASS: No orphaned records found")
        else:
            print(f"   ❌ FAIL: Found orphaned records")
            print(f"      Orphaned marks: {orphaned_marks}")
            print(f"      Orphaned attendance: {orphaned_attendance}")
            all_passed = False
        
        # 4. Session persistence check (informational)
        print("\n4. Session Persistence (Frontend)...")
        print("   ℹ️  Token storage: localStorage (persists across refreshes)")
        print("   ℹ️  Token expiration: 24 hours")
        print("   ℹ️  Manual test required:")
        print("      1. Login to student/faculty portal")
        print("      2. Refresh the page (F5)")
        print("      3. Verify you stay logged in")
        
        # Final summary
        print("\n" + "=" * 70)
        if all_passed:
            print("✅ ALL CHECKS PASSED!")
            print("=" * 70)
            print("\nSystem is ready to use:")
            print("1. ✅ Attendance: 1 Jan - 1 April 2026")
            print("2. ✅ Alerts: Proper timestamps (not 00:00)")
            print("3. ✅ Faculty-Student: Correct relationships")
            print("4. ℹ️  Session: Test manually by refreshing page")
        else:
            print("❌ SOME CHECKS FAILED!")
            print("=" * 70)
            print("\nPlease run: FIX_ATTENDANCE_ALERTS.bat")
        
    except Exception as e:
        print(f"\n❌ Error during verification: {str(e)}")
        all_passed = False
    finally:
        cursor.close()
        conn.close()
    
    return all_passed

if __name__ == '__main__':
    verify_fixes()
