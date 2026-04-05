import sys
sys.path.insert(0, 'backend')
import oracledb
from config import Config

conn = oracledb.connect(user=Config.DB_USER, password=Config.DB_PASSWORD, dsn=Config.DB_DSN)
cursor = conn.cursor()

# Check for rohan.sharma
cursor.execute("SELECT email, name, password FROM users WHERE email LIKE '%rohan.sharma%' AND ROWNUM <= 5")
print("Students with 'rohan.sharma':")
for row in cursor.fetchall():
    print(f"  Email: {row[0]}")
    print(f"  Name: {row[1]}")
    print(f"  Password: {row[2]}")
    print()

# Get first 5 students
cursor.execute("SELECT email, name FROM users WHERE role = 'student' AND ROWNUM <= 5")
print("\nFirst 5 students:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")

# Get all faculty
cursor.execute("SELECT email, name FROM users WHERE role = 'faculty'")
print("\nAll faculty:")
for row in cursor.fetchall():
    print(f"  {row[0]} - {row[1]}")

cursor.close()
conn.close()
