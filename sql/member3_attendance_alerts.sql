-- Member 3: Gurleen (Attendance & Alerts)
-- Attendance Table
CREATE TABLE attendance (
    attendance_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    subject_id NUMBER NOT NULL,
    attendance_date DATE NOT NULL,
    status CHAR(1) NOT NULL CHECK (status IN ('P', 'A')),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);
CREATE SEQUENCE attendance_seq START WITH 1 INCREMENT BY 1;

-- Alerts Table
CREATE TABLE alerts (
    alert_id NUMBER PRIMARY KEY,
    student_id NUMBER NOT NULL,
    alert_type VARCHAR2(20) NOT NULL CHECK (alert_type IN ('Warning', 'Alert', 'Critical')),
    message VARCHAR2(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
CREATE SEQUENCE alerts_seq START WITH 1 INCREMENT BY 1;