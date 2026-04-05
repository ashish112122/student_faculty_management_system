"""
Update marks distribution from old (MST:50, EST:100, Quiz:10, Assignment:20)
to new (MST:30, EST:40, Quiz:15, Assignment:15)
"""
import sys
sys.path.insert(0, 'backend')
import oracledb
from config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def update_marks():
    print("=" * 80)
    print("UPDATING MARKS DISTRIBUTION")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get current marks
        cursor.execute("SELECT COUNT(*) FROM marks")
        total_marks = cursor.fetchone()[0]
        print(f"\nTotal marks records: {total_marks}")
        
        # Update max_marks for each assessment type
        updates = [
            ('MST', 30),
            ('EST', 40),
            ('Quiz', 15),
            ('Assignment', 15)
        ]
        
        for assessment_type, new_max in updates:
            # Get old max
            cursor.execute("""
                SELECT DISTINCT max_marks FROM marks 
                WHERE assessment_type = :type AND ROWNUM = 1
            """, {'type': assessment_type})
            result = cursor.fetchone()
            old_max = result[0] if result else 0
            
            # Update max_marks
            cursor.execute("""
                UPDATE marks 
                SET max_marks = :new_max
                WHERE assessment_type = :type
            """, {'new_max': new_max, 'type': assessment_type})
            
            updated = cursor.rowcount
            
            # Scale marks_obtained proportionally
            if old_max > 0:
                cursor.execute("""
                    UPDATE marks 
                    SET marks_obtained = ROUND((marks_obtained / :old_max) * :new_max, 2)
                    WHERE assessment_type = :type
                """, {'old_max': old_max, 'new_max': new_max, 'type': assessment_type})
            
            print(f"   {assessment_type}: {old_max} → {new_max} marks ({updated} records updated)")
        
        conn.commit()
        
        # Verify updates
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)
        
        for assessment_type, expected_max in updates:
            cursor.execute("""
                SELECT MIN(max_marks), MAX(max_marks), COUNT(*) 
                FROM marks WHERE assessment_type = :type
            """, {'type': assessment_type})
            min_max, max_max, count = cursor.fetchone()
            status = "✓" if min_max == expected_max and max_max == expected_max else "✗"
            print(f"{status} {assessment_type}: max_marks = {expected_max} ({count} records)")
        
        print("\n" + "=" * 80)
        print("✓ MARKS DISTRIBUTION UPDATED SUCCESSFULLY")
        print("=" * 80)
        print("\nNew Distribution:")
        print("  MST: 30 marks")
        print("  EST: 40 marks")
        print("  Quiz: 15 marks")
        print("  Assignment: 15 marks")
        print("  Total: 100 marks")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    update_marks()
