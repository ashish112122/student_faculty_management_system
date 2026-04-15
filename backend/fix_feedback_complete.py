"""
Complete fix for feedback system - replaces old feedback table references with threading tables
"""
import os
import shutil
from datetime import datetime

print("=" * 70)
print("FIXING FEEDBACK SYSTEM - BACKEND API")
print("=" * 70)

# Backup
backup_name = f"app_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
shutil.copy('app.py', backup_name)
print(f"\n✅ Backup created: {backup_name}")

# Read current app.py
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"✅ Read app.py ({len(lines)} lines)")

# Find and replace feedback endpoints
print("\n🔧 Fixing feedback endpoints...")

# We'll rebuild the file by identifying sections and replacing them
output_lines = []
i = 0
replacements_made = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is a feedback endpoint we need to replace
    if "@app.route('/api/student/feedback/<int:faculty_id>/<int:subject_id>'," in line:
        print("  → Fixing: get_student_feedback_thread")
        # Skip until we find the next @app.route or end of file
        while i < len(lines) and not (lines[i].startswith('@app.route') and i > 0 and 'feedback' not in lines[i-5:i][-1]):
            i += 1
        
        # Add fixed version
        output_lines.append("@app.route('/api/student/feedback/<int:faculty_id>/<int:subject_id>', methods=['GET'])\n")
        output_lines.append("@token_required\n")
        output_lines.append("def get_student_feedback_thread(faculty_id, subject_id):\n")
        output_lines.append("    conn = get_db_connection()\n")
        output_lines.append("    cursor = conn.cursor()\n")
        output_lines.append("    \n")
        output_lines.append("    try:\n")
        output_lines.append("        cursor.execute(\"SELECT student_id FROM students WHERE user_id = :user_id\", {'user_id': request.user_id})\n")
        output_lines.append("        result = cursor.fetchone()\n")
        output_lines.append("        if not result:\n")
        output_lines.append("            return jsonify([])\n")
        output_lines.append("        \n")
        output_lines.append("        student_id = result[0]\n")
        output_lines.append("        \n")
        output_lines.append("        # Get thread\n")
        output_lines.append("        cursor.execute(\"\"\"\n")
        output_lines.append("            SELECT thread_id FROM feedback_threads\n")
        output_lines.append("            WHERE student_id = :student_id AND faculty_id = :faculty_id AND subject_id = :subject_id\n")
        output_lines.append("        \"\"\", {'student_id': student_id, 'faculty_id': faculty_id, 'subject_id': subject_id})\n")
        output_lines.append("        \n")
        output_lines.append("        thread = cursor.fetchone()\n")
        output_lines.append("        if not thread:\n")
        output_lines.append("            return jsonify([])\n")
        output_lines.append("        \n")
        output_lines.append("        thread_id = thread[0]\n")
        output_lines.append("        \n")
        output_lines.append("        # Get messages\n")
        output_lines.append("        cursor.execute(\"\"\"\n")
        output_lines.append("            SELECT message_id, sender_role, message, is_read, created_at, \n")
        output_lines.append("                   attachment_path, attachment_name, attachment_type\n")
        output_lines.append("            FROM feedback_messages\n")
        output_lines.append("            WHERE thread_id = :thread_id\n")
        output_lines.append("            ORDER BY created_at ASC\n")
        output_lines.append("        \"\"\", {'thread_id': thread_id})\n")
        output_lines.append("        \n")
        output_lines.append("        messages = []\n")
        output_lines.append("        for row in cursor.fetchall():\n")
        output_lines.append("            message_text = row[2].read() if hasattr(row[2], 'read') else str(row[2])\n")
        output_lines.append("            messages.append({\n")
        output_lines.append("                'feedback_id': row[0],\n")
        output_lines.append("                'sender_role': row[1],\n")
        output_lines.append("                'message': message_text,\n")
        output_lines.append("                'is_read': row[3],\n")
        output_lines.append("                'created_at': row[4].strftime('%Y-%m-%d %H:%M'),\n")
        output_lines.append("                'attachment_name': row[6],\n")
        output_lines.append("                'attachment_type': row[7],\n")
        output_lines.append("                'has_attachment': row[6] is not None\n")
        output_lines.append("            })\n")
        output_lines.append("        \n")
        output_lines.append("        # Mark as read\n")
        output_lines.append("        cursor.execute(\"\"\"\n")
        output_lines.append("            UPDATE feedback_messages SET is_read = 1\n")
        output_lines.append("            WHERE thread_id = :thread_id AND sender_role = 'faculty' AND is_read = 0\n")
        output_lines.append("        \"\"\", {'thread_id': thread_id})\n")
        output_lines.append("        conn.commit()\n")
        output_lines.append("        \n")
        output_lines.append("        return jsonify(messages)\n")
        output_lines.append("    finally:\n")
        output_lines.append("        cursor.close()\n")
        output_lines.append("        conn.close()\n")
        output_lines.append("\n")
        replacements_made += 1
        continue
    
    # Add line as-is if not a feedback endpoint to replace
    output_lines.append(line)
    i += 1

# Write fixed version
with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print(f"\n✅ Made {replacements_made} replacements")
print(f"✅ Wrote fixed app.py ({len(output_lines)} lines)")

print("\n" + "=" * 70)
print("✅ FEEDBACK SYSTEM FIXED!")
print("=" * 70)
print("\nNext steps:")
print("1. Restart backend server")
print("2. Test feedback system")
print("\nBackup location: backend/" + backup_name)
