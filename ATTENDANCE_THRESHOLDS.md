# 📊 ATTENDANCE THRESHOLDS & ALERT SYSTEM

## 🎯 Attendance Thresholds

### Current System Configuration

The system uses the following attendance thresholds to generate alerts:

| Threshold | Alert Type | Color | Description |
|-----------|------------|-------|-------------|
| **≥ 75%** | ✅ No Alert | Green | Good attendance - No action needed |
| **50% - 74%** | ⚠️ Warning | Yellow | Low attendance - Warning issued |
| **< 50%** | 🚨 Critical | Red | Very low attendance - Critical alert |

---

## 📋 Detailed Breakdown

### 1. Good Attendance (≥ 75%)
- **Status**: ✅ Satisfactory
- **Alert**: None
- **Action**: No action required
- **Display**: Normal attendance percentage shown
- **Example**: 80% attendance = No alert

### 2. Warning Level (50% - 74%)
- **Status**: ⚠️ Warning
- **Alert Type**: "Warning"
- **Alert Color**: Yellow (when read), Red (when unread)
- **Message**: "Low attendance in [Subject]: [Percentage]%"
- **Action**: Student should improve attendance
- **Example**: 68% attendance = Warning alert

### 3. Critical Level (< 50%)
- **Status**: 🚨 Critical
- **Alert Type**: "Critical"
- **Alert Color**: Red (unread), Yellow (read)
- **Message**: "Low attendance in [Subject]: [Percentage]%"
- **Action**: Immediate attention required
- **Example**: 45% attendance = Critical alert

---

## 🔄 Alert Generation Process

### When Alerts are Generated

1. **During Initial Setup**
   - System calculates attendance for all students
   - Generates alerts for students below 75%
   - Dates spread over last 30 days

2. **After Faculty Marks Attendance**
   - System recalculates attendance percentage
   - Checks if percentage < 75%
   - Creates new alert if threshold crossed
   - Updates existing alerts if needed

3. **Real-time Updates**
   - Alerts update immediately after attendance marking
   - Student sees updated alerts on next login/refresh
   - Percentage recalculated automatically

---

## 📊 Calculation Method

### Formula
```
Attendance Percentage = (Present Classes / Total Classes) × 100
```

### Example Calculation
```
Total Classes: 87
Present: 60
Absent: 27

Percentage = (60 / 87) × 100 = 68.97%

Result: Warning Alert (because 68.97% < 75%)
```

---

## 🎨 Alert Display

### In Student Portal

**Unread Alert** (Red):
```
┌─────────────────────────────────────┐
│ ⚠️ Warning                          │
│ Low attendance in Algorithms: 68%   │
│ 2026-04-05 10:30                    │
└─────────────────────────────────────┘
```

**Read Alert** (Yellow):
```
┌─────────────────────────────────────┐
│ ⚠️ Warning                          │
│ Low attendance in Algorithms: 68%   │
│ 2026-04-05 10:30                    │
└─────────────────────────────────────┘
```

---

## 🔧 Configuration Details

### Backend Code Location
File: `backend/app.py`

Function: `update_attendance_alerts()`

```python
# Check for low attendance (< 75%)
cursor.execute("""
    SELECT s.student_id, sub.subject_name,
           COUNT(*) as total,
           SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present
    FROM students s
    JOIN attendance a ON s.student_id = a.student_id
    JOIN subjects sub ON a.subject_id = sub.subject_id
    WHERE s.class_name = :class_name AND a.subject_id = :subject_id
    GROUP BY s.student_id, sub.subject_name
    HAVING (SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) < 0.75
""")

# Determine alert type
alert_type = 'Critical' if percentage < 50 else 'Warning'
```

---

## 📈 Threshold Modification Guide

### To Change Thresholds

If you want to modify the attendance thresholds, update these locations:

#### 1. Backend Alert Generation
File: `backend/app.py`
Line: ~820

Change:
```python
# Current: < 0.75 (75%)
HAVING (SUM(...) / COUNT(*)) < 0.75

# To change to 80%:
HAVING (SUM(...) / COUNT(*)) < 0.80
```

#### 2. Critical Threshold
File: `backend/app.py`
Line: ~830

Change:
```python
# Current: < 50%
alert_type = 'Critical' if percentage < 50 else 'Warning'

# To change to 40%:
alert_type = 'Critical' if percentage < 40 else 'Warning'
```

#### 3. Setup Script
File: `backend/setup_complete_system.py`
Line: ~375

Change:
```python
# Current: < 0.75
HAVING (SUM(...) / COUNT(*)) < 0.75

# To change to 80%:
HAVING (SUM(...) / COUNT(*)) < 0.80
```

---

## 📊 Current System Statistics

### Alert Distribution (Example)

Based on 300 students × 5 subjects = 1,500 student-subject pairs:

- **Good Attendance (≥75%)**: ~874 pairs (58%)
- **Warning (50-74%)**: ~520 pairs (35%)
- **Critical (<50%)**: ~106 pairs (7%)
- **Total Alerts Generated**: 626

### Date Distribution

Alerts are spread over the last 30 days:
- Most recent: April 5, 2026
- Oldest: March 6, 2026
- Distribution: Evenly spread (20-21 alerts per day)

---

## 🎯 Best Practices

### For Students
1. Check alerts regularly
2. Aim for ≥75% attendance in all subjects
3. Take action immediately if alert appears
4. Mark alerts as read after viewing

### For Faculty
1. Mark attendance regularly
2. System auto-generates alerts
3. No manual alert creation needed
4. Alerts update after each attendance marking

### For Administrators
1. Monitor alert statistics
2. Adjust thresholds if needed
3. Review critical alerts regularly
4. Ensure system is generating alerts correctly

---

## 🔍 Verification

### Check Alert Generation

Run this query to see alert distribution:
```sql
SELECT alert_type, COUNT(*) as count
FROM alerts
GROUP BY alert_type;
```

Expected output:
```
Warning: ~520
Critical: ~106
```

### Check Attendance Calculation

Run this query for a specific student:
```sql
SELECT 
    sub.subject_name,
    COUNT(*) as total,
    SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) as present,
    ROUND((SUM(CASE WHEN a.status = 'P' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) as percentage
FROM attendance a
JOIN subjects sub ON a.subject_id = sub.subject_id
WHERE a.student_id = 104
GROUP BY sub.subject_name;
```

---

## 📝 Summary

**Current Thresholds**:
- ✅ Good: ≥ 75%
- ⚠️ Warning: 50% - 74%
- 🚨 Critical: < 50%

**Alert Features**:
- Auto-generated after attendance marking
- Color-coded (Red/Yellow)
- Shows actual creation date
- Subject-specific
- Real-time updates

**Calculation**:
- Based on Present/Total ratio
- Percentage rounded to 2 decimals
- Checked after each attendance update

---

**Last Updated**: April 5, 2026  
**System Version**: 1.0  
**Status**: ✅ Operational
