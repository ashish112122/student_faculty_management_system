-- DATABASE TRIGGERS
-- TRIGGER 1: update_thread_timestamp
-- Purpose : Keep feedback thread metadata current
-- Table   : feedback_messages
-- Event   : AFTER INSERT

CREATE OR REPLACE TRIGGER update_thread_timestamp
AFTER INSERT ON feedback_messages
FOR EACH ROW
BEGIN
    UPDATE feedback_threads
    SET last_message_at = CURRENT_TIMESTAMP
    WHERE thread_id = :NEW.thread_id;
END;
/

-- TRIGGER 2: trg_attendance_alert
-- Purpose : Automatically generate alerts when attendance falls below threshold
-- Table   : attendance
-- Event   : AFTER INSERT OR UPDATE
-- Fires   : Once per row, after each attendance record is inserted or updated

CREATE OR REPLACE TRIGGER trg_attendance_alert
AFTER INSERT OR UPDATE ON attendance
FOR EACH ROW
DECLARE
    v_total       NUMBER;
    v_present     NUMBER;
    v_percentage  NUMBER;
    v_alert_type  VARCHAR2(20);
    v_message     VARCHAR2(500);
    v_subject_name VARCHAR2(100);
    v_existing    NUMBER;
BEGIN
    -- Get total and present count for this student-subject combination
    SELECT COUNT(*),
           SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END)
    INTO v_total, v_present
    FROM attendance
    WHERE student_id = :NEW.student_id
      AND subject_id = :NEW.subject_id;

    -- Avoid division by zero
    IF v_total = 0 THEN
        RETURN;
    END IF;

    -- Calculate attendance percentage using SQL
    v_percentage := ROUND((v_present / v_total) * 100, 2);

    -- Get subject name for the alert message
    SELECT subject_name INTO v_subject_name
    FROM subjects
    WHERE subject_id = :NEW.subject_id;

    -- Determine alert type based on percentage thresholds
    IF v_percentage < 50 THEN
        v_alert_type := 'Critical';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Attendance is critically low.';
    ELSIF v_percentage < 65 THEN
        v_alert_type := 'Alert';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Immediate action required.';
    ELSIF v_percentage < 75 THEN
        v_alert_type := 'Warning';
        v_message := 'Low attendance in ' || v_subject_name || ': ' || v_percentage || '%. Please improve attendance.';
    ELSE
        -- Attendance is acceptable (>= 75%), no alert needed
        -- If a previous alert exists for this student-subject, it remains in history
        RETURN;
    END IF;

    -- Check if an alert of this type already exists for this student-subject
    -- to avoid duplicate alerts
    SELECT COUNT(*) INTO v_existing
    FROM alerts
    WHERE student_id = :NEW.student_id
      AND subject_id = :NEW.subject_id
      AND alert_type = v_alert_type;

    -- Only insert if no duplicate exists
    IF v_existing = 0 THEN
        INSERT INTO alerts (
            alert_id,
            student_id,
            subject_id,
            alert_type,
            message,
            is_read,
            created_at
        )
        VALUES (
            alerts_seq.NEXTVAL,
            :NEW.student_id,
            :NEW.subject_id,
            v_alert_type,
            v_message,
            0,
            SYSDATE
        );
    ELSE
        -- Update existing alert message with latest percentage
        UPDATE alerts
        SET message    = v_message,
            is_read    = 0,
            created_at = SYSDATE
        WHERE student_id = :NEW.student_id
          AND subject_id  = :NEW.subject_id
          AND alert_type  = v_alert_type;
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        NULL; -- Subject not found, skip silently
    WHEN OTHERS THEN
        NULL; -- Do not let trigger failure break attendance marking
END;
/
