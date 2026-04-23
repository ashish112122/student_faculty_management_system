"""
Setup Oracle Database - Create Tables and Insert Demo Data
Run this script to automatically set up your database
"""

import oracledb
import os

# Database credentials
DB_USER = 'system'
DB_PASSWORD = 'Vanshi@Oracle1'
DB_DSN = 'localhost:1521/XE'

def read_sql_file(filename):
    """Read SQL file and return content"""
    filepath = os.path.join('database', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def execute_sql_script(cursor, sql_content, script_name):
    """Execute SQL script with proper handling"""
    print(f"\n{'='*50}")
    print(f"Executing {script_name}...")
    print('='*50)
    
    # Split by semicolon and slash for PL/SQL blocks
    statements = []
    current_statement = []
    in_plsql_block = False
    
    for line in sql_content.split('\n'):
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('--'):
            continue
        
        # Check for PL/SQL block
        if line.upper().startswith('BEGIN'):
            in_plsql_block = True
        
        current_statement.append(line)
        
        # End of statement
        if line.endswith(';') and not in_plsql_block:
            stmt = ' '.join(current_statement)
            if stmt.strip():
                statements.append(stmt)
            current_statement = []
        elif line == '/' and in_plsql_block:
            # End of PL/SQL block
            stmt = ' '.join(current_statement[:-1])  # Remove the '/'
            if stmt.strip():
                statements.append(stmt)
            current_statement = []
            in_plsql_block = False
    
    # Execute each statement
    success_count = 0
    error_count = 0
    
    for i, statement in enumerate(statements, 1):
        try:
            cursor.execute(statement)
            success_count += 1
            
            # Show progress for long operations
            if i % 10 == 0:
                print(f"  Executed {i}/{len(statements)} statements...")
                
        except oracledb.DatabaseError as e:
            error, = e.args
            # Ignore "name already used" errors (tables already exist)
            if error.code == 955:
                print(f"  ⚠ Table/sequence already exists (skipping)")
            else:
                print(f"  ❌ Error in statement {i}: {error.message}")
                error_count += 1
    
    print(f"\n✓ Completed: {success_count} successful, {error_count} errors")
    return error_count == 0

def main():
    print("="*50)
    print("Oracle Database Setup")
    print("="*50)
    print(f"\nConnecting to Oracle...")
    print(f"User: {DB_USER}")
    print(f"DSN: {DB_DSN}")
    
    try:
        # Connect to database
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        
        print("✓ Connected successfully!")
        
        cursor = connection.cursor()
        
        # Step 1: Create tables (schema.sql)
        print("\n" + "="*50)
        print("Step 1: Creating Tables")
        print("="*50)
        
        schema_sql = read_sql_file('schema.sql')
        
        # Execute schema statements one by one
        for statement in schema_sql.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                    print("✓", end=" ", flush=True)
                except oracledb.DatabaseError as e:
                    error, = e.args
                    if error.code == 955:  # Object already exists
                        print("⚠", end=" ", flush=True)
                    else:
                        print(f"\n❌ Error: {error.message}")
        
        connection.commit()
        print("\n✓ Tables created successfully!")
        
        # Step 2: Insert demo data
        print("\n" + "="*50)
        print("Step 2: Inserting Demo Data")
        print("="*50)
        print("This may take 1-2 minutes...")
        
        demo_sql = read_sql_file('demo_data.sql')
        
        # Split and execute
        statements = demo_sql.split(';')
        total = len([s for s in statements if s.strip() and not s.strip().startswith('--')])
        count = 0
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    # Handle PL/SQL blocks
                    if 'BEGIN' in statement.upper() and 'END' in statement.upper():
                        cursor.execute(statement)
                        print(f"\n✓ PL/SQL block executed")
                    else:
                        cursor.execute(statement)
                        count += 1
                        if count % 10 == 0:
                            print(f"  {count}/{total} statements...", end="\r")
                except oracledb.DatabaseError as e:
                    error, = e.args
                    print(f"\n⚠ Warning: {error.message}")
        
        connection.commit()
        print(f"\n✓ Demo data inserted successfully!")
        
        # Step 3: Verify
        print("\n" + "="*50)
        print("Step 3: Verification")
        print("="*50)
        
        tables = [
            ('USERS', 50),
            ('STUDENTS', 40),
            ('FACULTY', 10),
            ('SUBJECTS', 5),
            ('STUDENT_SUBJECTS', 200),
            ('MARKS', 800),
            ('ATTENDANCE', 6000),
            ('ALERTS', 3)
        ]
        
        all_good = True
        for table_name, expected_count in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                actual_count = cursor.fetchone()[0]
                
                if actual_count >= expected_count:
                    print(f"✓ {table_name}: {actual_count} records")
                else:
                    print(f"⚠ {table_name}: {actual_count} records (expected ~{expected_count})")
                    all_good = False
            except:
                print(f"❌ {table_name}: Table not found")
                all_good = False
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*50)
        if all_good:
            print("✅ Database Setup Complete!")
        else:
            print("⚠ Setup completed with warnings")
        print("="*50)
        print("\nYou can now run the application:")
        print("  python app.py")
        print("\nOr use the batch file:")
        print("  RUN_PROJECT.bat")
        
    except oracledb.DatabaseError as e:
        error, = e.args
        print(f"\n❌ Database Error:")
        print(f"  Code: {error.code}")
        print(f"  Message: {error.message}")
        print("\nCommon solutions:")
        print("1. Check Oracle service is running (services.msc)")
        print("2. Verify password: Vanshi@Oracle1")
        print("3. Ensure Oracle XE is installed")
        
    except FileNotFoundError as e:
        print(f"\n❌ File Error: {e}")
        print("\nMake sure you're running this from the backend folder:")
        print("  cd backend")
        print("  python setup_database.py")
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")

if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
