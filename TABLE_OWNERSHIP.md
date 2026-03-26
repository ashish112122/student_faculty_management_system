# Database Table Ownership

## Member 1 Tables (Login & Student Module)

| Table Name | Purpose | Created By | Used By |
|------------|---------|------------|---------|
| users | Store login credentials and basic user info | Member 1 | All Members |
| students | Store student profile and academic info | Member 1 | All Members |
| subjects | Store subject information | Member 1 | All Members |
| student_subjects | Map students to their enrolled subjects | Member 1 | All Members |
| feedback | Store student-faculty communication threads | Member 1 | Member 1 |

## Member 2 Tables (Faculty & Marks Module)

| Table Name | Purpose | Created By | Used By |
|------------|---------|------------|---------|
| faculty | Store faculty profile information | Member 2 | All Members |
| marks | Store student marks for all assessments | Member 2 | Member 1, Member 2 |

## Member 3 Tables (Attendance & Alerts)

| Table Name | Purpose | Created By | Used By |
|------------|---------|------------|---------|
| attendance | Store daily attendance records | Member 3 | Member 1, Member 3 |
| alerts | Store auto-generated attendance alerts | Member 3 | Member 1, Member 3 |

## Naming Convention
All tables use **snake_case** naming convention to ensure consistency across the project.

## Integration Notes
- All members can read from `users`, `students`, `subjects`, and `student_subjects`
- Member 1 reads from `marks`, `attendance`, and `alerts` (created by others)
- No duplicate tables
- Clear foreign key relationships
- Merge-safe architecture
