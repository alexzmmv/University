USE University;
GO

-- Stored procedure to add Student, Course, and their relationship
-- If any insertion fails, all operations will be rolled back
CREATE OR ALTER PROCEDURE sp_AddStudentCourse
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
    
    -- Validate input parameters
    IF (dbo.uf_ValidateFirstLetterUppercase(@studentName) = 0)
    BEGIN
        RAISERROR('Student name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@dateOfBirth) = 0)
    BEGIN
        RAISERROR('Date of birth must be a valid date in the past', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateEmail(@studentEmail) = 0)
    BEGIN
        RAISERROR('Student email format is invalid', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePhone(@studentPhone) = 0)
    BEGIN
        RAISERROR('Student phone number format is invalid', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidatePastDate(@enrollmentDate) = 0)
    BEGIN
        RAISERROR('Enrollment date must be a valid date in the past', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateFirstLetterUppercase(@profileName) = 0)
    BEGIN
        RAISERROR('Profile name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateFirstLetterUppercase(@courseName) = 0)
    BEGIN
        RAISERROR('Course name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateSemester(@semester) = 0)
    BEGIN
        RAISERROR('Semester must be between 1 and 8', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateCreditHours(@creditHours) = 0)
    BEGIN
        RAISERROR('Credit hours must be between 1 and 6', 16, 1);
        RETURN;
    END
    
    IF (dbo.uf_ValidateFirstLetterUppercase(@facultyName) = 0)
    BEGIN
        RAISERROR('Faculty name must start with uppercase letter', 16, 1);
        RETURN;
    END
    
    -- Variables for IDs
    DECLARE @facultyID INT;
    DECLARE @profileID INT;
    DECLARE @studentID INT;
    DECLARE @courseID INT;
    
    -- Start transaction
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Insert log entry for operation start
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('START', 'Student_Course_Procedure', 'Starting procedure with student ' + @studentName);
        
        -- Get Faculty ID
        SELECT @facultyID = Faculty_ID FROM Faculties WHERE Name = @facultyName;
        
        IF @facultyID IS NULL
        BEGIN
            RAISERROR('Faculty not found: %s', 16, 1, @facultyName);
            THROW 50001, 'Faculty not found', 1;
        END
        
        -- Get Profile ID
        SELECT @profileID = Profile_ID FROM Profiles WHERE Name = @profileName;
        
        IF @profileID IS NULL
        BEGIN
            RAISERROR('Profile not found: %s', 16, 1, @profileName);
            THROW 50002, 'Profile not found', 1;
        END
        
        -- Check if student email already exists
        IF EXISTS (SELECT 1 FROM Students WHERE Email = @studentEmail)
        BEGIN
            RAISERROR('Student with email %s already exists', 16, 1, @studentEmail);
            THROW 50003, 'Student email already exists', 1;
        END
        
        -- Check if course code already exists
        IF EXISTS (SELECT 1 FROM Courses WHERE Code = @courseCode)
        BEGIN
            RAISERROR('Course with code %s already exists', 16, 1, @courseCode);
            THROW 50004, 'Course code already exists', 1;
        END
        
        -- Insert Student
        INSERT INTO Students (Name, DateOfBirth, Email, Phone, EnrollmentDate, Profile_ID)
        VALUES (@studentName, @dateOfBirth, @studentEmail, @studentPhone, @enrollmentDate, @profileID);
        
        SET @studentID = SCOPE_IDENTITY();
        
        -- Log student insertion
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT', 'Students', 'Added student ' + @studentName + ' with ID ' + CAST(@studentID AS VARCHAR(10)));
        
        -- Insert Course
        INSERT INTO Courses (Code, Name, Semester, Credit_Hours, Description, Faculty_ID)
        VALUES (@courseCode, @courseName, @semester, @creditHours, @courseDescription, @facultyID);
        
        SET @courseID = SCOPE_IDENTITY();
        
        -- Log course insertion
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT', 'Courses', 'Added course ' + @courseName + ' with ID ' + CAST(@courseID AS VARCHAR(10)));
        
        -- Insert Student_Course relationship
        INSERT INTO Student_Courses (Student_ID, Course_ID, EnrollmentDate)
        VALUES (@studentID, @courseID, GETDATE());
        
        -- Log relationship insertion
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('INSERT', 'Student_Courses', 'Added relationship between Student ID ' + CAST(@studentID AS VARCHAR(10)) + 
               ' and Course ID ' + CAST(@courseID AS VARCHAR(10)));
        
        -- All operations successful, commit the transaction
        COMMIT TRANSACTION;
        
        -- Log success
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('SUCCESS', 'ALL', 'Successfully added student, course, and relationship');
        
    END TRY
    BEGIN CATCH
        -- An error occurred, roll back the transaction
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        -- Log the error
        INSERT INTO LogTable (TypeOperation, TableOperation, ExtraInfo)
        VALUES ('ERROR', ERROR_PROCEDURE(), 
                'Error: ' + ERROR_MESSAGE() + 
                ' at Line: ' + CAST(ERROR_LINE() AS VARCHAR(10)) + 
                ' State: ' + CAST(ERROR_STATE() AS VARCHAR(10)));
        
        -- Re-throw the error with additional info
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH;
END;
GO
