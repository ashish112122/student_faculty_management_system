-- Add attachment support to feedback table
-- Run this SQL script in Oracle SQL Developer or SQL*Plus

-- Add attachment_path column to store file path
ALTER TABLE feedback ADD (
    attachment_path VARCHAR2(500),
    attachment_name VARCHAR2(255),
    attachment_type VARCHAR2(50)
);

-- Commit changes
COMMIT;

-- Verify the changes
DESC feedback;

-- Check if columns were added
SELECT column_name, data_type, data_length 
FROM user_tab_columns 
WHERE table_name = 'FEEDBACK'
ORDER BY column_id;
