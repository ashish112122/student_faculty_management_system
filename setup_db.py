import oracledb

DB_CONFIG = {
    'user': 'system',
    'password': 'Vanshi@Oracle1',
    'dsn': 'localhost:1521/XE'
}

def run_sql_file(filename):
    conn = oracledb.connect(**DB_CONFIG)
    cursor = conn.cursor()
    with open(filename, 'r') as f:
        sql = f.read()
    # Split by ; for multiple statements
    statements = sql.split(';')
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except oracledb.DatabaseError:
                pass  # Ignore errors like already exists or does not exist
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run_sql_file('sql/create_tables.sql')
    run_sql_file('sql/insert_sample_data.sql')
    print("Database setup complete")