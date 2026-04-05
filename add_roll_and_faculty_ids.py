"""
Add roll numbers to students and faculty IDs to faculty table
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

def add_columns():
    print("=" * 80)
    print("ADDING ROLL NUMBERS AND FACULTY IDs")
    print("=" * 80)
    
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 1. Add roll_number column to students table
        print("\n1. Adding roll_number column to students table...")
        try:
            cursor.execute("ALTER TABLE students ADD roll_number NUMBER")
            print("   ✓ Column added")
        except Exception as e:
            if "ORA-01430" in str(e):
                print("   ✓ Column already exists")
            else:
                print(f"   ✗ Error: {str(e)}")
        
        # 2. Add faculty_code column to faculty table
        print("\n2. Adding faculty_code column to faculty table...")
        try:
            cursor.execute("ALTER TABLE faculty ADD faculty_code VARCHAR2(10)")
            print("   ✓ Column added")
        except Exception as e:
            if "ORA-01430" in str(e):
                print("   ✓ Column already exists")
            else:
                print(f"   ✗ Error: {str(e)}")
        
        conn.commit()
        
        # 3. Assign roll numbers to students (1-30 per batch)
        print("\n3. Assigning roll numbers to students...")
        for batch in BATCHES:
            cursor.execute("""
                SELECT student_id FROM students 
                WHERE class_name = :batch 
                ORDER BY name
            """, {'batch': batch})
            
            students = cursor.fetchall()
            roll = 1
            for (student_id,) in students:
                cursor.execute("""
                    UPDATE students 
                    SET roll_number = :roll 
                    WHERE student_id = :student_id
                """, {'roll': roll, 'student_id': student_id})
                roll += 1
            
            print(f"   ✓ {batch}: Assigned rolls 1-{len(students)}")
        
        conn.commit()
        
        # 4. Assign faculty codes
        print("\n4. Assigning faculty codes...")
        cursor.execute("SELECT faculty_id, name FROM faculty ORDER BY faculty_id")
        faculty_list = cursor.fetchall()
        
        for idx, (faculty_id, name) in enumerate(faculty_list, 1):
            faculty_code = f"FAC{idx:03d}"
            cursor.execute("""
                UPDATE faculty 
                SET faculty_code = :code 
                WHERE faculty_id = :faculty_id
            """, {'code': faculty_code, 'faculty_id': faculty_id})
            print(f"   ✓ {name}: {faculty_code}")
        
        conn.commit()
        
        # 5. Verify
        print("\n" + "=" * 80)
        print("VERIFICATION")
        print("=" * 80)
        
        # Check students
        print("\nSample Students with Roll Numbers:")
        cursor.execute("""
            SELECT name, class_name, roll_number 
            FROM students 
            WHERE ROWNUM <= 5 
            ORDER BY class_name, roll_number
        """)
        for name, batch, roll in cursor.fetchall():
            print(f"  ✓ {batch} - Roll {roll}: {name}")
        
        # Check faculty
        print("\nFaculty with Codes:")
        cursor.execute("SELECT name, faculty_code FROM faculty ORDER BY faculty_id")
        for name, code in cursor.fetchall():
            print(f"  ✓ {code}: {name}")
        
        print("\n" + "=" * 80)
        print("✓ ROLL NUMBERS AND FACULTY IDs ADDED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    add_columns()
