"""
Update faculty assignments to 3 batches each (as per requirement)
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

BATCHES = ['2Q31', '2Q32', '2Q33', '2Q34', '2Q35', '2Q36', '2Q37', '2Q38', '2Q39', '2Q40']

def update_assignments():
    print("=" * 80)
    print("UPDATING FACULTY ASSIGNMENTS TO 3 BATCHES EACH")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get faculty and subjects
        cursor.execute("SELECT faculty_id, name FROM faculty ORDER BY faculty_id")
        faculty = cursor.fetchall()
        
        cursor.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_id")
        subjects = cursor.fetchall()
        
        # Clear existing assignments
        cursor.execute("DELETE FROM faculty_classes")
        deleted = cursor.rowcount
        print(f"\nDeleted {deleted} old assignments")
        
        # Create new assignments: each faculty teaches 1 subject to 3 batches
        print("\nCreating new assignments (3 batches per faculty)...")
        
        # Faculty 1: Batches 2Q31, 2Q32, 2Q33
        # Faculty 2: Batches 2Q33, 2Q34, 2Q35
        # Faculty 3: Batches 2Q35, 2Q36, 2Q37
        # Faculty 4: Batches 2Q37, 2Q38, 2Q39
        # Faculty 5: Batches 2Q39, 2Q40, 2Q31
        
        faculty_batch_assignments = [
            [0, 1, 2],   # Faculty 1: 2Q31, 2Q32, 2Q33
            [2, 3, 4],   # Faculty 2: 2Q33, 2Q34, 2Q35
            [4, 5, 6],   # Faculty 3: 2Q35, 2Q36, 2Q37
            [6, 7, 8],   # Faculty 4: 2Q37, 2Q38, 2Q39
            [8, 9, 0]    # Faculty 5: 2Q39, 2Q40, 2Q31
        ]
        
        assignment_count = 0
        for i, (fac_id, fac_name) in enumerate(faculty):
            subj_id, subj_name = subjects[i]
            batch_indices = faculty_batch_assignments[i]
            assigned_batches = [BATCHES[idx] for idx in batch_indices]
            
            print(f"\n{fac_name} → {subj_name}:")
            
            for batch in assigned_batches:
                cursor.execute("""
                    INSERT INTO faculty_classes (faculty_class_id, faculty_id, subject_id, class_name)
                    VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :subj_id, :class_name)
                """, {'fac_id': fac_id, 'subj_id': subj_id, 'class_name': batch})
                assignment_count += 1
                print(f"  ✓ {batch}")
        
        conn.commit()
        
        print("\n" + "=" * 80)
        print(f"✓ CREATED {assignment_count} FACULTY ASSIGNMENTS")
        print("=" * 80)
        
        # Verify
        print("\nVerification:")
        cursor.execute("""
            SELECT f.name, sub.subject_name, COUNT(fc.class_name) as batch_count,
                   LISTAGG(fc.class_name, ', ') WITHIN GROUP (ORDER BY fc.class_name) as batches
            FROM faculty f
            JOIN faculty_classes fc ON f.faculty_id = fc.faculty_id
            JOIN subjects sub ON fc.subject_id = sub.subject_id
            GROUP BY f.name, sub.subject_name
            ORDER BY f.name
        """)
        
        for row in cursor.fetchall():
            print(f"  ✓ {row[0]} → {row[1]} → {row[2]} batches ({row[3]})")
        
        # Check coverage
        print("\nCoverage Check:")
        cursor.execute("""
            SELECT COUNT(DISTINCT s.class_name || '-' || sub.subject_id) as covered
            FROM students s
            CROSS JOIN subjects sub
            WHERE EXISTS (
                SELECT 1 FROM faculty_classes fc
                WHERE fc.subject_id = sub.subject_id AND fc.class_name = s.class_name
            )
        """)
        covered = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(DISTINCT class_name || '-' || subject_id)
            FROM students CROSS JOIN subjects
        """)
        total = cursor.fetchone()[0]
        
        print(f"  Covered: {covered}/{total} batch-subject combinations")
        
        if covered < total:
            print(f"\n⚠ Note: {total - covered} batch-subject combinations not covered")
            print("  This is expected as each faculty teaches only 3 batches")
            print("  Students in uncovered batches will not have faculty for some subjects")
        
        print("\n" + "=" * 80)
        print("✓ FACULTY ASSIGNMENTS UPDATED TO 3 BATCHES EACH")
        print("=" * 80)
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    update_assignments()
