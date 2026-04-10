"""
Add attachment support to feedback table
Run this script to add attachment columns to the database
"""
import oracledb
from config import Config

def add_attachment_columns():
    """Add attachment columns to feedback table"""
    try:
        conn = oracledb.connect(
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            dsn=Config.DB_DSN
        )
        cursor = conn.cursor()
        
        print("Adding attachment columns to feedback table...")
        
        # Check if columns already exist
        cursor.execute("""
            SELECT COUNT(*) 
            FROM user_tab_columns 
            WHERE table_name = 'FEEDBACK' 
            AND column_name IN ('ATTACHMENT_PATH', 'ATTACHMENT_NAME', 'ATTACHMENT_TYPE')
        """)
        
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"⚠️  {existing_count} attachment column(s) already exist. Skipping...")
        else:
            # Add columns
            cursor.execute("""
                ALTER TABLE feedback ADD (
                    attachment_path VARCHAR2(500),
                    attachment_name VARCHAR2(255),
                    attachment_type VARCHAR2(50)
                )
            """)
            
            conn.commit()
            print("✅ Attachment columns added successfully!")
        
        # Verify
        cursor.execute("""
            SELECT column_name, data_type, data_length 
            FROM user_tab_columns 
            WHERE table_name = 'FEEDBACK'
            AND column_name IN ('ATTACHMENT_PATH', 'ATTACHMENT_NAME', 'ATTACHMENT_TYPE')
            ORDER BY column_name
        """)
        
        print("\n📊 Attachment columns:")
        for row in cursor.fetchall():
            print(f"   - {row[0]}: {row[1]}({row[2]})")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database updated successfully!")
        print("You can now use attachments in feedback messages.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_attachment_columns()
