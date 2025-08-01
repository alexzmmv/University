USE University;
GO

-- Clean any previous test data
PRINT 'Cleaning previous test data...';
DELETE FROM Student_Courses WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Test%');
DELETE FROM Students WHERE Name LIKE 'Test%';
DELETE FROM Courses WHERE Code LIKE 'TEST%';
DELETE FROM LogTable;

-- Display test data
SELECT 'Test data has been cleaned' AS Status;
GO

-- TEST CASE 1: Successfully adding a student, course and their relationship
PRINT '---------------------- TEST CASE 1: SUCCESS SCENARIO ----------------------';
PRINT 'Attempting to add valid student, course and their relationship';

-- Check the current state before executing
SELECT COUNT(*) AS Students_Before FROM Students WHERE Name LIKE 'Test%';
SELECT COUNT(*) AS Courses_Before FROM Courses WHERE Code LIKE 'TEST%';
SELECT COUNT(*) AS Student_Courses_Before FROM Student_Courses;

-- Execute the stored procedure with valid data
EXEC sp_AddStudentCourse
    @studentName = 'Test Student',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'test.student@university.edu',
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'TEST101',
    @courseName = 'Test Course',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This is a test course for testing the stored procedure',
    @facultyName = 'Computer Science';

-- Check the state after execution
SELECT COUNT(*) AS Students_After FROM Students WHERE Name LIKE 'Test%';
SELECT COUNT(*) AS Courses_After FROM Courses WHERE Code LIKE 'TEST%';
SELECT COUNT(*) AS Student_Courses_After FROM Student_Courses;

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- TEST CASE 2: Failure scenario - Invalid email format
PRINT '---------------------- TEST CASE 2: FAILURE SCENARIO - INVALID EMAIL ----------------------';
PRINT 'Attempting to add student with invalid email (should fail)';

-- Check the current state before executing
SELECT COUNT(*) AS Students_Before FROM Students WHERE Name LIKE 'Test Invalid%';
SELECT COUNT(*) AS Courses_Before FROM Courses WHERE Code LIKE 'TEST201%';

-- Execute the stored procedure with invalid email
EXEC sp_AddStudentCourse
    @studentName = 'Test Invalid Email',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'invalid-email', -- Invalid email format
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'TEST201',
    @courseName = 'Test Course Invalid',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This course should not be added due to validation failure',
    @facultyName = 'Computer Science';

-- Check the state after execution - should be unchanged
SELECT COUNT(*) AS Students_After FROM Students WHERE Name LIKE 'Test Invalid%';
SELECT COUNT(*) AS Courses_After FROM Courses WHERE Code LIKE 'TEST201%';

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- TEST CASE 3: Failure scenario - Invalid faculty name
PRINT '---------------------- TEST CASE 3: FAILURE SCENARIO - NON-EXISTENT FACULTY ----------------------';
PRINT 'Attempting to add with non-existent faculty (should fail within transaction)';

-- Check the current state before executing
SELECT COUNT(*) AS Students_Before FROM Students WHERE Name LIKE 'Test Faculty%';
SELECT COUNT(*) AS Courses_Before FROM Courses WHERE Code LIKE 'TEST301%';

-- Execute the stored procedure with non-existent faculty
EXEC sp_AddStudentCourse
    @studentName = 'Test Faculty Error',
    @dateOfBirth = '2000-01-01',
    @studentEmail = 'test.faculty@university.edu',
    @studentPhone = '+40-721-555-4321',
    @enrollmentDate = '2022-09-01',
    @profileName = 'Software Engineering',
    @courseCode = 'TEST301',
    @courseName = 'Test Course Faculty',
    @semester = 1,
    @creditHours = 3,
    @courseDescription = 'This course should not be added due to non-existent faculty',
    @facultyName = 'Non-Existent Faculty';

-- Check the state after execution - should be unchanged
SELECT COUNT(*) AS Students_After FROM Students WHERE Name LIKE 'Test Faculty%';
SELECT COUNT(*) AS Courses_After FROM Courses WHERE Code LIKE 'TEST301%';

-- View the log entries
SELECT TOP 10 * FROM LogTable ORDER BY ExecutionDate DESC;

-- Display final summary
PRINT '---------------------- TEST SUMMARY ----------------------';
SELECT 
    (SELECT COUNT(*) FROM Students WHERE Name LIKE 'Test%') AS Total_Test_Students,
    (SELECT COUNT(*) FROM Courses WHERE Code LIKE 'TEST%') AS Total_Test_Courses,
    (SELECT COUNT(*) FROM Student_Courses 
     WHERE Student_ID IN (SELECT Student_ID FROM Students WHERE Name LIKE 'Test%')) AS Total_Test_Relationships;
GO
