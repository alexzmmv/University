USE University;
GO

-- Stored procedure that tries to recover as much as possible
-- If student insert succeeds but course fails, student will remain in the database
CREATE OR ALTER PROCEDURE sp_AddStudentCourseWithPartialRecovery
    @studentName VARCHAR(100),
    @dateOfBirth DATE,
    @studentEmail VARCHAR(100),
    @studentPhone VARCHAR(15),
    @enrollmentDate DATE,
    @profileName VARCHAR(100),
    @courseCode VARCHAR(20),
    @courseName VARCHAR(100),
    @semester INT,
    @creditHours INT,
    @courseDescription VARCHAR(500),
    @facultyName VARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Variables to track success of each step
    DECLARE @studentInserted BIT = 0;
    DECLARE @courseInserted BIT = 0;
    DECLARE @studentID INT;
    DECLARE @courseID INT;
    DECLARE @facultyID INT;
    DECLARE @profileID INT;
    
    -- Log the start of the procedure
    INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
    VALUES ('START', 'Student_Course_Recovery_Procedure', 'Starting procedure with partial recovery feature');
    
    -- Validate student data
    IF (dbo.uf_ValidateFirstLetterUppercase(@studentName) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Student name must start with uppercase letter');
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@dateOfBirth) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Date of birth must be a valid date in the past');
        RETURN;
    END
    
    IF (dbo.uf_ValidateEmail(@studentEmail) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Student email format is invalid');
        RETURN;
    END
    
    IF (dbo.uf_ValidatePhone(@studentPhone) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Student phone number format is invalid');
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@enrollmentDate) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Enrollment date must be a valid date in the past');
        RETURN;
    END
    
    -- Get Faculty ID
    SELECT @facultyID = Faculty_ID FROM Faculties WHERE Name = @facultyName;
    
    IF @facultyID IS NULL
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Faculty_Search', 'Faculty not found: ' + @facultyName);
        RETURN;
    END
    
    -- Get Profile ID
    SELECT @profileID = Profile_ID FROM Profiles WHERE Name = @profileName AND Faculty_ID = @facultyID;
    
    IF @profileID IS NULL
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Profile_Search', 'Profile not found: ' + @profileName + ' in faculty: ' + @facultyName);
        RETURN;
    END
    
    -- Validate course data
    IF (dbo.uf_ValidateFirstLetterUppercase(@courseName) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Course name must start with uppercase letter');
        RETURN;
    END
    
    IF (dbo.uf_ValidateSemester(@semester) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Semester must be between 1 and 8');
        RETURN;
    END
    
    IF (dbo.uf_ValidateCreditHours(@creditHours) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Credit hours must be between 1 and 6');
        RETURN;
    END
    
    IF (dbo.uf_ValidateCourseCode(@courseCode) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Validation', 'Course code must be in format XXX#### (3 uppercase letters followed by 4 digits)');
        RETURN;
    END
    
    -- PART 1: Try to insert student
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Check if student email already exists
        IF EXISTS (SELECT 1 FROM Students WHERE Email = @studentEmail)
        BEGIN
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('ERROR', 'Student_Insert', 'Student with email ' + @studentEmail + ' already exists');
            ROLLBACK TRANSACTION;
        END
        ELSE
        BEGIN
            -- Insert Student
            INSERT INTO Students (Name, DateOfBirth, Email, Phone, EnrollmentDate, Profile_ID)
            VALUES (@studentName, @dateOfBirth, @studentEmail, @studentPhone, @enrollmentDate, @profileID);
            
            SET @studentID = SCOPE_IDENTITY();
            SET @studentInserted = 1;
            
            -- Log student insertion
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('INSERT', 'Students', 'Added student ' + @studentName + ' with ID ' + CAST(@studentID AS VARCHAR(10)));
            
            COMMIT TRANSACTION;
        END
    END TRY
    BEGIN CATCH
        -- If student insert fails, log error and rollback
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Student_Insert', 'Failed to add student: ' + ERROR_MESSAGE());
    END CATCH;
    
    -- PART 2: Try to insert course (even if student insert failed)
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Check if course code already exists
        IF EXISTS (SELECT 1 FROM Courses WHERE Code = @courseCode)
        BEGIN
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('ERROR', 'Course_Insert', 'Course with code ' + @courseCode + ' already exists');
            ROLLBACK TRANSACTION;
        END
        ELSE
        BEGIN
            -- Insert Course
            INSERT INTO Courses (Code, Name, Semester, Credit_Hours, Description, Faculty_ID)
            VALUES (@courseCode, @courseName, @semester, @creditHours, @courseDescription, @facultyID);
            
            SET @courseID = SCOPE_IDENTITY();
            SET @courseInserted = 1;
            
            -- Log course insertion
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('INSERT', 'Courses', 'Added course ' + @courseName + ' with ID ' + CAST(@courseID AS VARCHAR(10)));
            
            COMMIT TRANSACTION;
        END
    END TRY
    BEGIN CATCH
        -- If course insert fails, log error and rollback
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Course_Insert', 'Failed to add course: ' + ERROR_MESSAGE());
    END CATCH;
    
    -- PART 3: Try to create relationship (only if both previous inserts succeeded)
    IF @studentInserted = 1 AND @courseInserted = 1
    BEGIN
        BEGIN TRY
            BEGIN TRANSACTION;
            
            -- Check if relationship already exists
            IF EXISTS (SELECT 1 FROM Student_Courses WHERE Student_ID = @studentID AND Course_ID = @courseID)
            BEGIN
                INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
                VALUES ('ERROR', 'Relationship_Insert', 'Relationship between student ID ' + CAST(@studentID AS VARCHAR(10)) +
                       ' and course ID ' + CAST(@courseID AS VARCHAR(10)) + ' already exists');
                ROLLBACK TRANSACTION;
            END
            ELSE
            BEGIN
                -- Insert relationship
                INSERT INTO Student_Courses (Student_ID, Course_ID, EnrollmentDate)
                VALUES (@studentID, @courseID, GETDATE());
                
                -- Log relationship insertion
                INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
                VALUES ('INSERT', 'Student_Courses', 'Added relationship between Student ID ' + CAST(@studentID AS VARCHAR(10)) +
                       ' and Course ID ' + CAST(@courseID AS VARCHAR(10)));
                
                COMMIT TRANSACTION;
            END
        END TRY
        BEGIN CATCH
            -- If relationship insert fails, log error and rollback
            IF @@TRANCOUNT > 0
                ROLLBACK TRANSACTION;
            
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('ERROR', 'Relationship_Insert', 'Failed to add relationship: ' + ERROR_MESSAGE());
        END CATCH;
    END
    
    -- Final summary
    INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
    VALUES ('END', 'Student_Course_Recovery_Procedure', 
           'Procedure completed. Student: ' + CASE WHEN @studentInserted = 1 THEN 'SUCCESS' ELSE 'FAILED' END +
           ', Course: ' + CASE WHEN @courseInserted = 1 THEN 'SUCCESS' ELSE 'FAILED' END +
           ', Relationship: ' + CASE WHEN @studentInserted = 1 AND @courseInserted = 1 THEN 'ATTEMPTED' ELSE 'SKIPPED' END);
END;
GO
