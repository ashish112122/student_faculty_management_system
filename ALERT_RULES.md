# Alert Rules

Alerts are given based on this logic: attendance is checked after every class entry,
and an alert is generated when a student's attendance in any subject falls below 75%.

---

## When Attendance is Checked

Attendance is checked immediately after every attendance record is inserted or updated.
There is no fixed number of days. The check happens in real time using a database trigger.

Trigger name : trg_attendance_alert
Table        : attendance
Event        : AFTER INSERT OR UPDATE ON attendance

Every time a faculty member marks attendance, the trigger fires automatically,
recalculates the percentage for that student and subject, and decides whether
an alert needs to be created.

---

## How Percentage is Calculated

Formula:

    Attendance Percentage = (Total Present / Total Classes) x 100

Example:
- Total classes held: 80
- Student was present: 55
- Percentage = (55 / 80) x 100 = 68.75%
- Result: Alert generated (below 75%)

The calculation uses all attendance records for that student in that subject,
from the first class to the most recent one.

---

## Alert Conditions

Three levels of alerts are used:

### Level 1: Warning

Condition  : Attendance is between 65% and 74.99%
Alert Type : Warning
Message    : Low attendance in [Subject]: [X]%. Please improve attendance.
Meaning    : Student is approaching the minimum threshold. Action recommended.

### Level 2: Alert

Condition  : Attendance is between 50% and 64.99%
Alert Type : Alert
Message    : Low attendance in [Subject]: [X]%. Immediate action required.
Meaning    : Attendance is significantly low. Immediate improvement needed.

### Level 3: Critical

Condition  : Attendance is below 50%
Alert Type : Critical
Message    : Low attendance in [Subject]: [X]%. Attendance is critically low.
Meaning    : Attendance has dropped to a critical level. Urgent action required.

### No Alert

Condition  : Attendance is 75% or above
Result     : No alert is generated. Student is within acceptable range.

---

## Summary Table

    Attendance %       Alert Type     Action Needed
    -------------------------------------------------------
    75% and above      None           No action required
    65% to 74.99%      Warning        Improve attendance
    50% to 64.99%      Alert          Immediate action
    Below 50%          Critical       Urgent action

---

## Duplicate Alert Handling

If an alert of the same type already exists for a student in a subject,
it is not inserted again. Instead, the existing alert is updated with
the latest percentage and marked as unread.

This prevents the alerts table from filling up with repeated entries
for the same condition.

---

## Which Table Stores Attendance

Table name : attendance

Columns used for calculation:
- student_id  : identifies the student
- subject_id  : identifies the subject
- status      : 'P' for Present, 'A' for Absent

---

## Which Table Stores Alerts

Table name : alerts

Columns:
- alert_id    : unique identifier
- student_id  : student who receives the alert
- subject_id  : subject the alert is about
- alert_type  : Warning, Alert, or Critical
- message     : full alert message text
- is_read     : 0 = unread, 1 = read
- created_at  : date and time the alert was generated

---

## Where the Logic Lives

The entire alert logic is written in SQL inside the database trigger.
No Python code is involved in generating alerts.

File : backend/database/triggers.sql
Trigger : trg_attendance_alert

The trigger runs inside Oracle Database automatically whenever attendance
is inserted or updated. The application does not need to call any function
to generate alerts.

---

## Viva Summary

- Alerts are checked after every attendance entry, not after a fixed number of days.
- The threshold for an alert is 75% attendance.
- Three alert levels exist: Warning (65-75%), Alert (50-65%), Critical (below 50%).
- The percentage is calculated as: (Present / Total) x 100.
- The attendance table is used for the calculation.
- The trigger trg_attendance_alert is responsible for generating alerts automatically.
- Alert logic is fully SQL-based, implemented as a database trigger.
