USE University;
GO

-- Clean the test data for fresh execution
PRINT 'Cleaning previous test data...';
DELETE FROM Student_Courses WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Partial%');
DELETE FROM Students WHERE Name LIKE 'Partial%';
DELETE FROM Courses WHERE Code LIKE 'PART%';
DELETE FROM LogTable;

-- Test Case 1: Complete Success - All operations should succeed
PRINT '---------------------- TEST CASE 1: COMPLETE SUCCESS ----------------------';
PRINT 'All operations should succeed';

-- Check the current state before executing
SELECT COUNT(*) AS Students_Before FROM Students WHERE Name LIKE 'Partial Test%';
SELECT COUNT(*) AS Courses_Before FROM Courses WHERE Code LIKE 'PART%';
SELECT COUNT(*) AS Student_Courses_Before FROM Student_Courses WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Partial Test%');

-- Execute the stored procedure with valid data
EXEC sp_AddStudentCourseWithPartialRecovery
    @studentName = 'Partial Test Success',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'partial.test@university.edu',
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'PART101',
    @courseName = 'Partial Recovery Test',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This is a test course for testing the partial recovery procedure',
    @facultyName = 'Computer Science';

-- Check the state after execution
SELECT * FROM Students WHERE Name LIKE 'Partial Test%';
SELECT * FROM Courses WHERE Code LIKE 'PART%';
SELECT * FROM Student_Courses WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Partial Test%');

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- Test Case 2: Partial Success - Student succeeds but course fails (duplicate code)
PRINT '---------------------- TEST CASE 2: PARTIAL SUCCESS - COURSE FAILS ----------------------';
PRINT 'Student should be added but course should fail due to duplicate code';

-- First, ensure we have a course with the code we'll try to duplicate
IF NOT EXISTS (SELECT 1 FROM Courses WHERE Code = 'PART999')
BEGIN
    INSERT INTO Courses (Code, Name, Semester, Credit_Hours, Description, Faculty_ID)
    VALUES ('PART999', 'Existing Course', 1, 3, 'This course already exists', 
           (SELECT TOP 1 Faculty_ID FROM Faculties WHERE Name = 'Computer Science'));
END

-- Check the current state before executing
SELECT COUNT(*) AS Students_Before FROM Students WHERE Name LIKE 'Partial Course%';
SELECT COUNT(*) AS Courses_Before FROM Courses WHERE Code = 'PART999';

-- Execute the stored procedure with duplicate course code
EXEC sp_AddStudentCourseWithPartialRecovery
    @studentName = 'Partial Course Failure',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'partial.course@university.edu',
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'PART999',  -- This code already exists
    @courseName = 'Duplicate Course Code',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This course should not be added due to duplicate code',
    @facultyName = 'Computer Science';

-- Check the state after execution - student should exist but no new course
SELECT * FROM Students WHERE Name LIKE 'Partial Course%';
SELECT * FROM Courses WHERE Code = 'PART999';
SELECT * FROM Student_Courses WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Partial Course%');

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- Test Case 3: Partial Success - Course succeeds but student fails (duplicate email)
PRINT '---------------------- TEST CASE 3: PARTIAL SUCCESS - STUDENT FAILS ----------------------';
PRINT 'Course should be added but student should fail due to duplicate email';

-- First, ensure we have a student with the email we'll try to duplicate
IF NOT EXISTS (SELECT 1 FROM Students WHERE Email = 'duplicate.email@university.edu')
BEGIN
    INSERT INTO Students (Name, DateOfBirth, Email, Phone, EnrollmentDate, Profile_ID)
    VALUES ('Existing Student', '2000-01-01', 'duplicate.email@university.edu', '+40-721-555-1111', '2022-09-01',
           (SELECT TOP 1 Profile_ID FROM Profiles WHERE Name = 'Software Engineering'));
END

-- Execute the stored procedure with duplicate student email
EXEC sp_AddStudentCourseWithPartialRecovery
    @studentName = 'Partial Student Failure',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'duplicate.email@university.edu',  -- This email already exists
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'PART888',
    @courseName = 'Student Duplicate Test',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This course should be added but student should fail',
    @facultyName = 'Computer Science';

-- Check the state after execution - course should exist but no new student
SELECT * FROM Students WHERE Name LIKE 'Partial Student%';
SELECT * FROM Courses WHERE Code = 'PART888';
SELECT * FROM Student_Courses WHERE Course_ID IN (SELECT Course_ID FROM Courses WHERE Code = 'PART888');

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- Display final summary
PRINT '---------------------- TEST SUMMARY ----------------------';
SELECT 
    (SELECT COUNT(*) FROM Students WHERE Name LIKE 'Partial%') AS Total_Partial_Students,
    (SELECT COUNT(*) FROM Courses WHERE Code LIKE 'PART%') AS Total_Partial_Courses,
    (SELECT COUNT(*) FROM Student_Courses 
     WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Partial%')) AS Total_Partial_Relationships;
GO
