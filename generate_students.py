import oracledb

DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def insert_students():
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        for i in range(2, 152):  # Start from 2 to avoid duplicates
            email = f'student{i}@univ.edu'
            password = 'pass123'
            name = f'Student {i}'
            dept = (i % 4) + 1
            try:
                cursor.execute("INSERT INTO users (user_id, email, password, name, role) VALUES (users_seq.NEXTVAL, :1, :2, :3, 'student')", (email, password, name))
                cursor.execute("INSERT INTO students (student_id, user_id, department_id, semester) VALUES (students_seq.NEXTVAL, users_seq.CURRVAL, :1, 4)", (dept,))
            except oracledb.IntegrityError:
                pass  # Duplicate email, skip
        conn.commit()
        print("Students inserted")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insert_students()