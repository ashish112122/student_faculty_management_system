import oracledb
from backend.config import Config

DB_CONFIG = {
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'dsn': Config.DB_DSN
}

def update_faculty_classes():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Updating faculty_classes table...")
        
        # Clear existing data
        cursor.execute("DELETE FROM faculty_classes")
        
        # Add new assignments
        assignments = [
            (6, '2Q11', 6), (6, '2Q12', 6),
            (7, '2Q11', 7),
            (8, '2Q12', 8),
            (9, '2Q11', 9), (9, '2Q12', 9),
            (10, '2Q11', 10), (10, '2Q12', 10),
        ]
        
        for fac_id, class_name, subj_id in assignments:
            cursor.execute("""
                INSERT INTO faculty_classes (faculty_class_id, faculty_id, class_name, subject_id)
                VALUES (faculty_classes_seq.NEXTVAL, :fac_id, :class_name, :subj_id)
            """, {'fac_id': fac_id, 'class_name': class_name, 'subj_id': subj_id})
        
        conn.commit()
        print(f"✓ Updated {len(assignments)} faculty-class assignments")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    update_faculty_classes()
