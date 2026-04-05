"""
Fix faculty assignments to ensure all students have faculty for all subjects
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

def fix_assignments():
    print("=" * 80)
    print("FIXING FACULTY ASSIGNMENTS")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Get faculty and subjects
        cursor.execute("SELECT faculty_id, name FROM faculty ORDER BY faculty_id")
        faculty = cursor.fetchall()
        
        cursor.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_id")
        subjects = cursor.fetchall()
        
        print(f"\nFaculty: {len(faculty)}")
        print(f"Subjects: {len(subjects)}")
        print(f"Batches: {len(BATCHES)}")
        
        # Clear existing assignments
        cursor.execute("DELETE FROM faculty_classes")
        deleted = cursor.rowcount
        print(f"\nDeleted {deleted} old assignments")
        
        # Create new assignments: each faculty teaches 1 subject to ALL batches
        # This ensures every student in every batch has a faculty for every subject
        print("\nCreating new assignments...")
        
        assignment_count = 0
        for i, (fac_id, fac_name) in enumerate(faculty):
            subj_id, subj_name = subjects[i]
            
            print(f"\n{fac_name} → {subj_name}:")
            
            # Assign this faculty to ALL batches for their subject
            for batch in BATCHES:
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
            SELECT f.name, sub.subject_name, COUNT(fc.class_name) as batch_count
            FROM faculty f
            JOIN faculty_classes fc ON f.faculty_id = fc.faculty_id
            JOIN subjects sub ON fc.subject_id = sub.subject_id
            GROUP BY f.name, sub.subject_name
            ORDER BY f.name
        """)
        
        for row in cursor.fetchall():
            print(f"  ✓ {row[0]} → {row[1]} → {row[2]} batches")
        
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
        
        if covered == total:
            print("\n" + "=" * 80)
            print("✓ ALL STUDENTS NOW HAVE FACULTY FOR ALL SUBJECTS")
            print("=" * 80)
        else:
            print(f"\n✗ Still missing {total - covered} assignments")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    fix_assignments()
