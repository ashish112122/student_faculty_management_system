# Complete Installation Guide for Windows

## Step 1: Install Oracle Database

### Option A: Oracle Database XE (Express Edition) - Recommended
1. Download Oracle Database 21c XE from:
   https://www.oracle.com/database/technologies/xe-downloads.html

2. Run the installer
3. Set password for SYS and SYSTEM users (remember this!)
4. Default port: 1521
5. Service name: XE

### Option B: Oracle Database 19c
1. Download from Oracle website
2. Follow installation wizard
3. Note your connection details

## Step 2: Install Python Dependencies

### Install from your downloaded wheel file:
```cmd
cd backend
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
pip install Flask==2.3.0
pip install flask-cors==4.0.0
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0
```

### Or install all at once:
```cmd
cd backend
pip install -r requirements.txt
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

## Step 3: Configure Database Connection

Edit `backend/config.py` with your Oracle credentials:

```python
DB_USER = 'system'           # Your Oracle username
DB_PASSWORD = 'your_password' # Your Oracle password
DB_DSN = 'localhost:1521/xe'  # Your Oracle connection string
```

## Step 4: Setup Database Schema

### Using SQL Developer (Recommended):
1. Download Oracle SQL Developer from:
   https://www.oracle.com/database/sqldeveloper/technologies/download/

2. Connect to your database:
   - Username: system
   - Password: (your password)
   - Hostname: localhost
   - Port: 1521
   - Service name: xe

3. Open and run these files in order:
   - `backend/database/schema.sql`
   - `backend/database/demo_data.sql`

### Using SQL*Plus (Command Line):
```cmd
sqlplus system/your_password@localhost:1521/xe

SQL> @backend/database/schema.sql
SQL> @backend/database/demo_data.sql
SQL> exit
```

## Step 5: Verify Installation

### Test Oracle Connection:
```cmd
cd backend
python
```

```python
import oracledb
conn = oracledb.connect(user='system', password='your_password', dsn='localhost:1521/xe')
print("Connected successfully!")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
print(f"Users in database: {cursor.fetchone()[0]}")
conn.close()
```

## Step 6: Run the Application

### Start Backend:
```cmd
cd backend
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Start Frontend:
```cmd
cd frontend
python -m http.server 8000
```

Open browser: http://localhost:8000/login.html

## Troubleshooting

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"

**Solution 1 - Use Thin Mode (No Oracle Client needed):**
Edit `backend/app.py` and `backend/utils/alert_checker.py`:
```python
# Add this line after imports
oracledb.init_oracle_client()  # Remove this line if present

# Use thin mode (default, no client needed)
def get_db_connection():
    return oracledb.connect(
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        dsn=DB_CONFIG['dsn']
    )
```

**Solution 2 - Install Oracle Instant Client:**
1. Download from: https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html
2. Extract to C:\oracle\instantclient_21_3
3. Add to PATH environment variable
4. Restart terminal

### Error: "ORA-12541: TNS:no listener"
- Check if Oracle service is running:
  ```cmd
  services.msc
  ```
  Look for "OracleServiceXE" and start it

### Error: "ORA-01017: invalid username/password"
- Verify your credentials in `backend/config.py`
- Reset password if needed:
  ```cmd
  sqlplus / as sysdba
  ALTER USER system IDENTIFIED BY new_password;
  ```

### Error: Module 'oracledb' not found
```cmd
pip install oracledb
```
Or use your wheel file:
```cmd
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl
```

## Demo Credentials

**Students:**
- rohan.sharma@thapar.edu / password123
- rahul.verma@thapar.edu / password123
- simran.kaur@thapar.edu / password123

**Faculty:**
- rohan.sharma@thaparfac.edu / password123
- neha.verma@thaparfac.edu / password123

## Quick Start Commands

```cmd
# Install everything
cd backend
pip install -r requirements.txt
pip install C:\Users\vansh\Downloads\oracledb-3.4.2-cp311-cp311-win_amd64.whl

# Setup database (in SQL Developer or SQL*Plus)
@backend/database/schema.sql
@backend/database/demo_data.sql

# Run backend
python app.py

# In new terminal, run frontend
cd frontend
python -m http.server 8000

# Open browser
http://localhost:8000/login.html
```

## Need Help?
- Oracle XE Documentation: https://docs.oracle.com/en/database/oracle/oracle-database/21/xeinw/
- Python oracledb: https://python-oracledb.readthedocs.io/
