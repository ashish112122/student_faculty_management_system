# Requirements Document

## Introduction

The Faculty & Marks Module (Member 2 — RAHUL branch) is a subsystem of the Student-Faculty Management System. It provides faculty profile management, marks entry, class management, result generation, and performance visualization via Chart.js bar charts. The module owns the `faculty` and `marks` tables and interacts with read-only tables (`users`, `students`, `subjects`, `student_subjects`) owned by other members. All backend logic lives in `/backend/faculty.py` and `/backend/marks.py`; all frontend logic lives in `/frontend/faculty.js` and `/frontend/marks.js`.

## Glossary

- **Faculty_Service**: The Flask backend module in `/backend/faculty.py` that handles faculty-related API endpoints.
- **Marks_Service**: The Flask backend module in `/backend/marks.py` that handles marks-related API endpoints.
- **Faculty_Dashboard**: The frontend view rendered by `/frontend/faculty.js` showing faculty profile and class summary.
- **Marks_UI**: The frontend view rendered by `/frontend/marks.js` for marks entry, result viewing, and performance charts.
- **faculty**: MySQL table owned by Member 2 with columns `faculty_id`, `name`, `email` (FK → users), `dept_id`, `designation`.
- **marks**: MySQL table owned by Member 2 with columns `marks_id`, `student_id` (FK → students), `subject_id` (FK → subjects), `marks_obtained`, `grade`, `exam_type`.
- **users**: Read-only MySQL table owned by Member 1 with columns `user_id`, `email`, `password`, `role`.
- **students**: Read-only MySQL table owned by Member 1 with columns `student_id`, `name`, `email`, `batch_year`, `semester`, `dept_id`, `cgpa`, `total_credits`.
- **subjects**: Read-only MySQL table owned by Member 1 with columns `subject_id`, `subject_name`.
- **student_subjects**: Read-only MySQL table owned by Member 1 linking students to subjects.
- **Parameterized_Query**: A SQL query that uses placeholders (e.g., `%s`) instead of string interpolation to prevent SQL injection.
- **Grade**: A letter grade (e.g., A, B, C, D, F) derived from `marks_obtained`.
- **exam_type**: A string identifying the type of examination (e.g., "midterm", "final", "internal").

---

## Requirements

### Requirement 1: Faculty Profile Management

**User Story:** As a faculty member, I want to view and update my profile, so that my department and designation information stays accurate in the system.

#### Acceptance Criteria

1. WHEN a valid `faculty_id` is provided, THE Faculty_Service SHALL return the corresponding faculty record including `name`, `email`, `dept_id`, and `designation`.
2. WHEN a faculty profile update request is received with valid `faculty_id`, `dept_id`, and `designation`, THE Faculty_Service SHALL update only the `faculty` table and return a success response.
3. IF a faculty profile update request is received with a `faculty_id` that does not exist in the `faculty` table, THEN THE Faculty_Service SHALL return an HTTP 404 response with a descriptive error message.
4. THE Faculty_Service SHALL use Parameterized_Query for all SELECT, INSERT, and UPDATE operations on the `faculty` table.
5. THE Faculty_Service SHALL perform only SELECT operations on the `users` table when resolving faculty email from `users.email`.

---

### Requirement 2: Faculty Dashboard

**User Story:** As a faculty member, I want a dashboard showing my assigned classes and student counts, so that I can get a quick overview of my teaching load.

#### Acceptance Criteria

1. WHEN a faculty member loads the Faculty_Dashboard, THE Faculty_Dashboard SHALL display the faculty's `name`, `dept_id`, and `designation` fetched from the `faculty` table.
2. WHEN the Faculty_Dashboard loads, THE Faculty_Service SHALL return the list of distinct `subject_id` values associated with marks records entered by that faculty member, by querying the `marks` table with a SELECT statement.
3. WHEN the Faculty_Dashboard loads, THE Faculty_Service SHALL return the count of distinct `student_id` values per `subject_id` from the `marks` table using a Parameterized_Query SELECT.
4. THE Faculty_Dashboard SHALL render the class summary data without modifying the `students`, `subjects`, or `student_subjects` tables.

---

### Requirement 3: Marks Entry

**User Story:** As a faculty member, I want to enter marks for students per subject and exam type, so that student performance is recorded accurately.

#### Acceptance Criteria

1. WHEN a marks entry request is received with valid `student_id`, `subject_id`, `marks_obtained`, and `exam_type`, THE Marks_Service SHALL insert a new record into the `marks` table and return an HTTP 201 response.
2. WHEN a marks entry request is received, THE Marks_Service SHALL validate that `marks_obtained` is a numeric value between 0 and 100 inclusive before inserting.
3. IF a marks entry request is received with a `marks_obtained` value outside the range 0–100, THEN THE Marks_Service SHALL return an HTTP 400 response with a descriptive error message and SHALL NOT insert any record.
4. IF a marks entry request is received with a `student_id` that does not exist in the `students` table, THEN THE Marks_Service SHALL return an HTTP 404 response with a descriptive error message.
5. IF a marks entry request is received with a `subject_id` that does not exist in the `subjects` table, THEN THE Marks_Service SHALL return an HTTP 404 response with a descriptive error message.
6. THE Marks_Service SHALL derive and store the `grade` field according to the following mapping: 90–100 → "A", 75–89 → "B", 60–74 → "C", 45–59 → "D", 0–44 → "F".
7. THE Marks_Service SHALL use Parameterized_Query for all INSERT operations on the `marks` table.
8. THE Marks_Service SHALL perform only SELECT operations on the `students` and `subjects` tables during validation.

---

### Requirement 4: Marks Update

**User Story:** As a faculty member, I want to correct previously entered marks, so that errors in student records can be fixed.

#### Acceptance Criteria

1. WHEN a marks update request is received with a valid `marks_id` and updated `marks_obtained`, THE Marks_Service SHALL update the corresponding record in the `marks` table and recalculate and store the `grade`.
2. IF a marks update request is received with a `marks_id` that does not exist in the `marks` table, THEN THE Marks_Service SHALL return an HTTP 404 response with a descriptive error message.
3. IF a marks update request is received with a `marks_obtained` value outside the range 0–100, THEN THE Marks_Service SHALL return an HTTP 400 response and SHALL NOT update any record.
4. THE Marks_Service SHALL use Parameterized_Query for all UPDATE operations on the `marks` table.

---

### Requirement 5: Result Generation

**User Story:** As a faculty member, I want to retrieve all marks records for a given subject and exam type, so that I can generate and review class results.

#### Acceptance Criteria

1. WHEN a result query is received with a valid `subject_id` and `exam_type`, THE Marks_Service SHALL return all matching records from the `marks` table joined with `student_name` from the `students` table and `subject_name` from the `subjects` table.
2. WHEN a result query is received with a valid `subject_id` and `exam_type`, THE Marks_Service SHALL return records sorted by `marks_obtained` in descending order.
3. IF a result query is received with a `subject_id` that has no records in the `marks` table for the given `exam_type`, THEN THE Marks_Service SHALL return an HTTP 200 response with an empty list.
4. THE Marks_Service SHALL use Parameterized_Query for all SELECT operations joining `marks`, `students`, and `subjects`.
5. THE Marks_Service SHALL perform only SELECT operations on the `students` and `subjects` tables during result generation.

---

### Requirement 6: Performance Charts

**User Story:** As a faculty member, I want to view a bar chart of student marks for a subject, so that I can visually assess class performance distribution.

#### Acceptance Criteria

1. WHEN a faculty member requests a performance chart for a given `subject_id` and `exam_type`, THE Marks_UI SHALL render a Chart.js bar chart displaying each student's `name` on the x-axis and `marks_obtained` on the y-axis.
2. WHEN the chart data is fetched, THE Marks_Service SHALL return a JSON array of objects each containing `student_name` and `marks_obtained`, sourced via a SELECT join on `marks` and `students`.
3. THE Marks_UI SHALL display a grade distribution summary (count of A, B, C, D, F grades) alongside the bar chart, derived from the same dataset returned by the Marks_Service.
4. IF the Marks_Service returns an empty dataset for the requested `subject_id` and `exam_type`, THEN THE Marks_UI SHALL display a message stating "No marks data available for the selected subject and exam type" instead of rendering a chart.

---

### Requirement 7: Data Integrity and Merge Safety

**User Story:** As a team member, I want the Faculty & Marks module to be merge-safe and non-destructive to other members' tables, so that integration does not break the shared codebase.

#### Acceptance Criteria

1. THE Faculty_Service SHALL perform INSERT and UPDATE operations exclusively on the `faculty` table.
2. THE Marks_Service SHALL perform INSERT and UPDATE operations exclusively on the `marks` table.
3. THE Faculty_Service and THE Marks_Service SHALL NOT execute any INSERT, UPDATE, or DELETE statement targeting the `users`, `students`, `subjects`, `student_subjects`, `feedback`, `attendance`, or `alerts` tables.
4. THE Faculty_Service and THE Marks_Service SHALL use Parameterized_Query for every SQL statement that includes user-supplied input.
5. WHERE the `subject_name` value is displayed in the Faculty_Dashboard or Marks_UI, THE Marks_Service SHALL retrieve it via a SELECT on the `subjects` table to ensure the name matches exactly with other modules.
