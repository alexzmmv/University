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
        VALUES ('VALIDATION_ERROR', 'Students', 'Student name must start with uppercase letter');
        RAISERROR('Student name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@dateOfBirth) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Students', 'Date of birth must be a valid date in the past');
        RAISERROR('Date of birth must be a valid date in the past', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateEmail(@studentEmail) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Students', 'Student email format is invalid');
        RAISERROR('Student email format is invalid', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePhone(@studentPhone) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Students', 'Student phone number format is invalid');
        RAISERROR('Student phone number format is invalid', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@enrollmentDate) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Students', 'Enrollment date must be a valid date in the past');
        RAISERROR('Enrollment date must be a valid date in the past', 16, 1);
        RETURN;
    END
    
    -- Get Faculty ID
    SELECT @facultyID = Faculty_ID FROM Faculties WHERE Name = @facultyName;
    
    IF @facultyID IS NULL
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Faculties', 'Faculty with the given name does not exist');
        RAISERROR('Faculty with the given name does not exist', 16, 1);
        RETURN;
    END
    
    -- Get Profile ID
    SELECT @profileID = Profile_ID FROM Profiles WHERE Name = @profileName AND Faculty_ID = @facultyID;
    
    IF @profileID IS NULL
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Profiles', 'Profile with the given name does not exist for this faculty');
        RAISERROR('Profile with the given name does not exist for this faculty', 16, 1);
        RETURN;
    END
    
    -- TRANSACTION 1: Insert Student
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO Students (Name, Date_of_Birth, Profile_ID, Email, Phone, Enrollment_Date)
        VALUES (@studentName, @dateOfBirth, @profileID, @studentEmail, @studentPhone, @enrollmentDate);
        
        SET @studentID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        SET @studentInserted = 1;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT_SUCCESS', 'Students', 'Inserted student with ID: ' + CAST(@studentID AS VARCHAR));
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT_ERROR', 'Students', 'Failed to insert student: ' + ERROR_MESSAGE());
        
        -- Return error details
        SELECT 
            ERROR_NUMBER() AS ErrorNumber,
            ERROR_SEVERITY() AS ErrorSeverity,
            ERROR_STATE() AS ErrorState,
            ERROR_PROCEDURE() AS ErrorProcedure,
            ERROR_LINE() AS ErrorLine,
            ERROR_MESSAGE() AS ErrorMessage;
        
        RETURN;
    END CATCH;
    
    -- Validate course data
    IF (dbo.uf_ValidateFirstLetterUppercase(@courseName) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Courses', 'Course name must start with uppercase letter');
        RAISERROR('Course name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateSemester(@semester) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Courses', 'Semester must be between 1 and 8');
        RAISERROR('Semester must be between 1 and 8', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateCreditHours(@creditHours) = 0)
    BEGIN
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('VALIDATION_ERROR', 'Courses', 'Credit hours must be between 1 and 6');
        RAISERROR('Credit hours must be between 1 and 6', 16, 1);
        RETURN;
    END
    
    -- TRANSACTION 2: Insert Course
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO Courses (Code, Name, Faculty_ID, Semester, Credit_Hours, Description)
        VALUES (@courseCode, @courseName, @facultyID, @semester, @creditHours, @courseDescription);
        
        SET @courseID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
        SET @courseInserted = 1;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT_SUCCESS', 'Courses', 'Inserted course with ID: ' + CAST(@courseID AS VARCHAR));
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT_ERROR', 'Courses', 'Failed to insert course: ' + ERROR_MESSAGE());
        
        -- Return error details but continue - we've already inserted the student
        SELECT 
            ERROR_NUMBER() AS ErrorNumber,
            ERROR_SEVERITY() AS ErrorSeverity,
            ERROR_STATE() AS ErrorState,
            ERROR_PROCEDURE() AS ErrorProcedure,
            ERROR_LINE() AS ErrorLine,
            ERROR_MESSAGE() AS ErrorMessage;
        
        -- We continue to return so that the student record is preserved
        SELECT 'Student was added but course failed' AS PartialSuccess;
        RETURN;
    END CATCH;
    
    -- TRANSACTION 3: Create relationship between Student and Course
    -- Only if both student and course were successfully inserted
    IF @studentInserted = 1 AND @courseInserted = 1
    BEGIN
        BEGIN TRY
            BEGIN TRANSACTION;
            
            INSERT INTO Student_Courses (Student_ID, Course_ID)
            VALUES (@studentID, @courseID);
            
            COMMIT TRANSACTION;
            
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('INSERT_SUCCESS', 'Student_Courses', 'Created relationship between student ID: ' 
                    + CAST(@studentID AS VARCHAR) + ' and course ID: ' + CAST(@courseID AS VARCHAR));
            
            -- Return success message
            SELECT 'Successfully added student, course and relationship' AS Result;
        END TRY
        BEGIN CATCH
            IF @@TRANCOUNT > 0
                ROLLBACK TRANSACTION;
            
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('INSERT_ERROR', 'Student_Courses', 'Failed to create relationship: ' + ERROR_MESSAGE());
            
            -- Return error details
            SELECT 
                ERROR_NUMBER() AS ErrorNumber,
                ERROR_SEVERITY() AS ErrorSeverity,
                ERROR_STATE() AS ErrorState,
                ERROR_PROCEDURE() AS ErrorProcedure,
                ERROR_LINE() AS ErrorLine,
                ERROR_MESSAGE() AS ErrorMessage;
            
            -- Return partial success information
            SELECT 'Student and Course were added but relationship failed' AS PartialSuccess;
        END CATCH;
    END
    
    -- Report success/failure summary
    INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
    VALUES ('SUMMARY', 'Student_Course_Recovery_Procedure', 
            'Student: ' + CASE WHEN @studentInserted = 1 THEN 'SUCCESS' ELSE 'FAILED' END + ', ' +
            'Course: ' + CASE WHEN @courseInserted = 1 THEN 'SUCCESS' ELSE 'FAILED' END + ', ' +
            'Relationship: ' + CASE WHEN @studentInserted = 1 AND @courseInserted = 1 THEN 'ATTEMPTED' ELSE 'SKIPPED' END);
END;
GO
    
    -- STEP 1: Try to insert student
    BEGIN TRY
        -- Validate student parameters
        IF (dbo.uf_ValidateFirstLetterUppercase(@studentName) = 0)
            RAISERROR('Student name must start with uppercase letter', 16, 1);
        
        IF (@dateOfBirth > GETDATE())
            RAISERROR('Date of birth cannot be in the future', 16, 1);
        
        IF (dbo.uf_ValidateEmail(@studentEmail) = 0)
            RAISERROR('Invalid email format', 16, 1);
        
        IF (dbo.uf_ValidatePhone(@studentPhone) = 0)
            RAISERROR('Invalid phone number format', 16, 1);
        
        IF (@enrollmentDate > GETDATE())
            RAISERROR('Enrollment date cannot be in the future', 16, 1);
        
        -- Get Profile ID
        DECLARE @profileID INT;
        DECLARE @facultyID INT;
        
        SELECT @facultyID = Faculty_ID FROM Faculties WHERE Name = @facultyName;
        IF @facultyID IS NULL
        BEGIN
            RAISERROR('Faculty not found', 16, 1);
        END
        
        SELECT @profileID = Profile_ID FROM Profiles WHERE Name = @profileName AND Faculty_ID = @facultyID;
        IF @profileID IS NULL
        BEGIN
            RAISERROR('Profile not found for the given faculty', 16, 1);
        END
        
        -- Begin transaction for student insert
        BEGIN TRANSACTION;
        
        -- Insert Student
        INSERT INTO Students (Name, Date_of_Birth, Profile_ID, Email, Phone, Enrollment_Date)
        VALUES (@studentName, @dateOfBirth, @profileID, @studentEmail, @studentPhone, @enrollmentDate);
        
        -- Get the inserted Student ID
        SET @studentID = SCOPE_IDENTITY();
        
        -- Log student insertion
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT', 'Students', 'Added student with ID: ' + CAST(@studentID AS VARCHAR));
        
        COMMIT TRANSACTION;
        SET @studentInserted = 1;
        
        SELECT 'Student inserted successfully with ID: ' + CAST(@studentID AS VARCHAR) AS [Result];
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        -- Log the error
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Students', 'Failed to add student: ' + ERROR_MESSAGE());
        
        SELECT 'Failed to insert student: ' + ERROR_MESSAGE() AS [StudentInsertResult];
    END CATCH
    
    -- STEP 2: Try to insert course
    BEGIN TRY
        -- Validate course parameters
        IF (dbo.uf_ValidateCourseCode(@courseCode) = 0)
            RAISERROR('Invalid course code format. It must be 3 uppercase letters followed by 4 digits', 16, 1);
        
        IF (dbo.uf_ValidateFirstLetterUppercase(@courseName) = 0)
            RAISERROR('Course name must start with uppercase letter', 16, 1);
        
        IF (dbo.uf_ValidateSemester(@semester) = 0)
            RAISERROR('Semester must be between 1 and 8', 16, 1);
        
        IF (dbo.uf_ValidateCreditHours(@creditHours) = 0)
            RAISERROR('Credit hours must be between 1 and 10', 16, 1);
            
        -- Begin transaction for course insert
        BEGIN TRANSACTION;
        
        -- Insert Course
        INSERT INTO Courses (Code, Name, Faculty_ID, Semester, Credit_Hours, Description)
        VALUES (@courseCode, @courseName, @facultyID, @semester, @creditHours, @courseDescription);
        
        -- Get the inserted Course ID
        SET @courseID = SCOPE_IDENTITY();
        
        -- Log course insertion
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT', 'Courses', 'Added course with ID: ' + CAST(@courseID AS VARCHAR));
        
        COMMIT TRANSACTION;
        SET @courseInserted = 1;
        
        SELECT 'Course inserted successfully with ID: ' + CAST(@courseID AS VARCHAR) AS [Result];
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
            
        -- Log the error
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', 'Courses', 'Failed to add course: ' + ERROR_MESSAGE());
        
        SELECT 'Failed to insert course: ' + ERROR_MESSAGE() AS [CourseInsertResult];
    END CATCH
    
    -- STEP 3: Try to create relationship only if both student and course were inserted
    IF @studentInserted = 1 AND @courseInserted = 1
    BEGIN
        BEGIN TRY
            -- Begin transaction for relationship insert
            BEGIN TRANSACTION;
            
            -- Insert the relationship in Student_Courses table
            INSERT INTO Student_Courses (Student_ID, Course_ID)
            VALUES (@studentID, @courseID);
            
            -- Log relationship insertion
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('INSERT', 'Student_Courses', 'Added relationship between Student ID: ' + CAST(@studentID AS VARCHAR) + ' and Course ID: ' + CAST(@courseID AS VARCHAR));
            
            COMMIT TRANSACTION;
            
            SELECT 'Relationship between student and course created successfully' AS [Result];
        END TRY
        BEGIN CATCH
            IF @@TRANCOUNT > 0
                ROLLBACK TRANSACTION;
                
            -- Log the error
            INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
            VALUES ('ERROR', 'Student_Courses', 'Failed to add relationship: ' + ERROR_MESSAGE());
            
            SELECT 'Failed to create relationship: ' + ERROR_MESSAGE() AS [RelationshipInsertResult];
        END CATCH
    END
    
    -- Final status
    SELECT 
        CASE 
            WHEN @studentInserted = 1 AND @courseInserted = 1 THEN 'Both student and course were inserted successfully'
            WHEN @studentInserted = 1 AND @courseInserted = 0 THEN 'Only student was inserted successfully'
            WHEN @studentInserted = 0 AND @courseInserted = 1 THEN 'Only course was inserted successfully'
            ELSE 'Both student and course insertion failed'
        END AS [FinalStatus];
        
    -- Log procedure completion
    INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
    VALUES ('END', 'Student_Course_Recovery_Procedure', 'Procedure completed');
END;
GO
