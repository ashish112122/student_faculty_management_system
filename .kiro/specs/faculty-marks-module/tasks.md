# Implementation Plan: Faculty & Marks Module

## Overview

Implement the Faculty & Marks Module (Member 2 — RAHUL branch) as two Flask blueprints, two JS files, three HTML templates, and four test files. All write operations are confined to the `faculty` and `marks` tables. Read-only access is used for `users`, `students`, and `subjects`.

## Tasks

- [x] 1. Database setup — create `faculty` and `marks` tables
  - Create `schema_member2.sql` (or equivalent init script) with `CREATE TABLE IF NOT EXISTS` for `faculty` and `marks` only
  - `faculty`: `faculty_id`, `name`, `email` (FK → users.email), `dept_id`, `designation`
  - `marks`: `marks_id`, `student_id` (FK → students), `subject_id` (FK → subjects), `marks_obtained`, `grade`, `exam_type`
  - Do NOT include DDL for `users`, `students`, `subjects`, `student_subjects`, `feedback`, `attendance`, or `alerts`
  - _Requirements: 7.1, 7.2, 7.3_

- [x] 2. Implement `derive_grade()` utility and `faculty.py` Flask blueprint
  - [x] 2.1 Implement `derive_grade(marks: float) -> str` in `/backend/faculty.py` (or a shared utils module imported by both blueprints)
    - 90–100 → "A", 75–89 → "B", 60–74 → "C", 45–59 → "D", 0–44 → "F"
    - _Requirements: 3.6, 4.1_
  - [x] 2.2 Implement `GET /faculty/profile/<faculty_id>`
    - Parameterized SELECT on `faculty`; JOIN with `users` for email
    - Return 200 with `{ faculty_id, name, email, dept_id, designation }` or 404
    - _Requirements: 1.1, 1.3, 1.4, 1.5_
  - [x] 2.3 Implement `POST /faculty/profile/update`
    - Validate `faculty_id` exists; parameterized UPDATE on `faculty` only
    - Return 200 on success, 404 if not found, 400 if required fields missing
    - _Requirements: 1.2, 1.3, 1.4, 7.1_
  - [x] 2.4 Implement `GET /faculty/dashboard`
    - Parameterized SELECT on `faculty` for profile; aggregate SELECT on `marks` JOIN `subjects` for class summary
    - Return combined JSON `{ profile, classes: [{ subject_id, subject_name, student_count }] }`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 7.5_
  - [ ]* 2.5 Write unit tests for `faculty.py` endpoints in `/tests/test_faculty_unit.py`
    - Happy-path GET profile, happy-path POST update, happy-path GET dashboard
    - 404 for unknown `faculty_id` on both GET and POST
    - 400 for missing required fields on POST update
    - _Requirements: 1.1, 1.2, 1.3, 2.1_

- [x] 3. Implement `marks.py` Flask blueprint
  - [x] 3.1 Implement `POST /marks/add`
    - Validate `marks_obtained` in [0, 100]; check `student_id` exists in `students`; check `subject_id` exists in `subjects` (both via parameterized SELECT COUNT)
    - Derive grade, parameterized INSERT into `marks`, return 201 with `{ message, marks_id }`
    - Return 400 for out-of-range marks, 404 for unknown student/subject
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_
  - [x] 3.2 Implement `PUT /marks/update/<marks_id>`
    - Validate `marks_obtained` in [0, 100]; check `marks_id` exists; recalculate grade; parameterized UPDATE
    - Return 200 with `{ message, grade }`, 400 for out-of-range, 404 for unknown `marks_id`
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  - [x] 3.3 Implement `GET /marks/results`
    - Parameterized SELECT joining `marks`, `students`, `subjects` filtered by `subject_id` and `exam_type`
    - Return list sorted by `marks_obtained` DESC; return empty list `[]` if no records
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  - [x] 3.4 Implement `GET /marks/chart-data`
    - Parameterized SELECT joining `marks` and `students` filtered by `subject_id` and `exam_type`
    - Return `[ { student_name, marks_obtained } ]`
    - _Requirements: 6.2, 7.4_
  - [ ]* 3.5 Write unit tests for `marks.py` endpoints in `/tests/test_marks_unit.py`
    - Happy-path POST add, PUT update, GET results, GET chart-data
    - 400 for marks out of range on add and update
    - 404 for unknown student_id, subject_id, marks_id
    - Empty list for GET results with no matching records
    - Boundary values for `derive_grade`: 0, 44, 45, 59, 60, 74, 75, 89, 90, 100
    - _Requirements: 3.1–3.8, 4.1–4.4, 5.1–5.5, 6.2_

- [ ] 4. Checkpoint — ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Property-based tests for `faculty.py` (Hypothesis)
  - [ ]* 5.1 Write property test for faculty profile lookup round-trip
    - **Property 1: Faculty Profile Lookup Round-Trip**
    - **Validates: Requirements 1.1**
    - Use `st.integers(min_value=1)` for faculty_id; insert then GET; assert all fields match
    - `@settings(max_examples=100)`
    - _File: `/tests/test_faculty_property.py`_
  - [ ]* 5.2 Write property test for faculty profile update round-trip
    - **Property 2: Faculty Profile Update Round-Trip**
    - **Validates: Requirements 1.2**
    - Use `st.integers()` for dept_id, `st.text()` for designation; POST update then GET; assert updated values returned
    - `@settings(max_examples=100)`
    - _File: `/tests/test_faculty_property.py`_
  - [ ]* 5.3 Write property test for dashboard aggregation accuracy
    - **Property 3: Dashboard Aggregation Accuracy**
    - **Validates: Requirements 2.1, 2.2, 2.3**
    - Use `st.lists(st.fixed_dictionaries({...}))` for marks records; assert distinct subjects and per-subject student counts match inserted data
    - `@settings(max_examples=100)`
    - _File: `/tests/test_faculty_property.py`_
  - [ ]* 5.4 Write property test for invalid faculty_id returns 404
    - **Property 7 (faculty side): Invalid ID Returns 404**
    - **Validates: Requirements 1.3**
    - Use `st.integers().filter(lambda x: x not in existing_ids)`; assert GET profile and POST update both return 404 and perform no writes
    - `@settings(max_examples=100)`
    - _File: `/tests/test_faculty_property.py`_

- [ ] 6. Property-based tests for `marks.py` (Hypothesis)
  - [ ]* 6.1 Write property test for marks range validation
    - **Property 4: Marks Range Validation**
    - **Validates: Requirements 3.2, 3.3, 4.3**
    - Use `st.floats().filter(lambda x: x < 0 or x > 100)`; assert POST add and PUT update both return 400 and leave `marks` table unchanged
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_
  - [ ]* 6.2 Write property test for grade derivation correctness
    - **Property 5: Grade Derivation Correctness**
    - **Validates: Requirements 3.6, 4.1**
    - Use `st.floats(min_value=0, max_value=100)`; assert stored grade matches expected bracket for both insert and update paths
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_
  - [ ]* 6.3 Write property test for marks insert round-trip
    - **Property 6: Marks Insert Round-Trip**
    - **Validates: Requirements 3.1**
    - Use `st.fixed_dictionaries({student_id, subject_id, marks_obtained, exam_type})`; assert POST add returns 201 and record is retrievable via GET results with correct fields
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_
  - [ ]* 6.4 Write property test for invalid marks_id / student_id / subject_id returns 404
    - **Property 7 (marks side): Invalid ID Returns 404**
    - **Validates: Requirements 3.4, 3.5, 4.2**
    - Use `st.integers().filter(lambda x: x not in existing_ids)`; assert relevant endpoints return 404 and perform no writes
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_
  - [ ]* 6.5 Write property test for result completeness and ordering
    - **Property 8: Result Completeness and Ordering**
    - **Validates: Requirements 5.1, 5.2**
    - Use `st.lists(marks_record_strategy, min_size=1)`; assert GET results returns exactly the matching records sorted by `marks_obtained` DESC
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_
  - [ ]* 6.6 Write property test for chart data structure
    - **Property 9: Chart Data Structure**
    - **Validates: Requirements 6.2**
    - Use `st.lists(marks_record_strategy)`; assert every object in GET chart-data response has non-empty `student_name` and `marks_obtained` in [0, 100]
    - `@settings(max_examples=100)`
    - _File: `/tests/test_marks_property.py`_

- [ ] 7. Checkpoint — ensure all backend + property tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement HTML templates
  - [x] 8.1 Create `/templates/faculty_dashboard.html`
    - Bootstrap 5 layout with a profile card (name, dept, designation) and a class-summary table (subject name, student count)
    - Include `<script src="faculty.js">` at bottom
    - _Requirements: 2.1, 2.4_
  - [x] 8.2 Create `/templates/add_marks.html`
    - Form fields: `student_id`, `subject_id`, `marks_obtained`, `exam_type`; inline validation error display area
    - Include `<script src="marks.js">` at bottom
    - _Requirements: 3.1, 3.2, 3.3_
  - [x] 8.3 Create `/templates/marks_report.html`
    - Results table (student name, subject, marks, grade, exam type) + `<canvas id="marksChart">` for Chart.js bar chart + grade distribution summary section
    - "No marks data available" message element (hidden by default, shown when dataset is empty)
    - Include Chart.js CDN script and `<script src="marks.js">` at bottom
    - _Requirements: 5.1, 6.1, 6.3, 6.4_

- [x] 9. Implement `faculty.js`
  - On `DOMContentLoaded`: read `faculty_id` from page context (meta tag or data attribute), call `GET /faculty/dashboard`, populate profile card fields and class-summary table rows
  - On profile-update form submit: collect `faculty_id`, `dept_id`, `designation`; call `POST /faculty/profile/update`; show success toast on 200, inline error on 400/404
  - _Requirements: 2.1, 1.2, 1.3_

- [x] 10. Implement `marks.js`
  - Marks entry: on add-form submit call `POST /marks/add`; display inline error for 400, toast for 404/500, clear form on 201
  - Marks update: on update-form submit call `PUT /marks/update/<marks_id>`; handle 400/404 responses
  - Results view: on subject/exam_type selection call `GET /marks/results`; render sortable HTML table
  - Chart view: call `GET /marks/chart-data`; if empty show "No marks data available" message; otherwise render Chart.js bar chart (student names on x-axis, marks on y-axis) and compute + display grade distribution (count of A/B/C/D/F) client-side from the same dataset
  - _Requirements: 6.1, 6.3, 6.4, 3.1, 4.1, 5.1_

- [x] 11. Final checkpoint — ensure all tests pass and templates render correctly
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- All SQL in `faculty.py` and `marks.py` must use parameterized queries (`%s` placeholders) — no string interpolation
- `faculty.py` and `marks.py` must never execute INSERT, UPDATE, or DELETE on `users`, `students`, `subjects`, `student_subjects`, `feedback`, `attendance`, or `alerts`
- Property tests use Hypothesis with `@settings(max_examples=100)` and include the tagging comment `# Feature: faculty-marks-module, Property <N>: <property_text>`
- Each correctness property (P1–P9) is covered by exactly one property-based test
