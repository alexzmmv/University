USE University;
GO

-- Transaction 1 for Dirty Reads demonstration - Will update a course and then rollback
-- Run this transaction first
CREATE OR ALTER PROCEDURE sp_DirtyReads_Transaction1
AS
BEGIN
    PRINT 'Starting Transaction 1 - will update course name and then rollback';
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- Update a course name - make sure the course with ID 1 exists
    IF EXISTS (SELECT 1 FROM Courses WHERE Course_ID = 1)
    BEGIN
        DECLARE @OldName VARCHAR(100);
        SELECT @OldName = Name FROM Courses WHERE Course_ID = 1;
        
        UPDATE Courses 
        SET Name = 'UNCOMMITTED COURSE NAME (WILL BE ROLLED BACK)' 
        WHERE Course_ID = 1;
        
        PRINT 'Transaction 1 - Updated course name from "' + @OldName + '" to "UNCOMMITTED COURSE NAME (WILL BE ROLLED BACK)", sleeping for 10 seconds...';
    END
    ELSE
    BEGIN
        PRINT 'Course with ID 1 does not exist. Creating a test course.';
        INSERT INTO Courses (Code, Name, Faculty_ID, Semester, Credit_Hours, Description)
        VALUES ('TEST001', 'Original Course Name', 
               (SELECT TOP 1 Faculty_ID FROM Faculties), 
               1, 3, 'Course used for dirty reads demonstration');
               
        DECLARE @NewID INT = SCOPE_IDENTITY();
        
        UPDATE Courses 
        SET Name = 'UNCOMMITTED COURSE NAME (WILL BE ROLLED BACK)' 
        WHERE Course_ID = @NewID;
        
        PRINT 'Transaction 1 - Created and updated course with ID ' + CAST(@NewID AS VARCHAR) + ', sleeping for 10 seconds...';
    END
    
    -- Wait to allow Transaction 2 to read this uncommitted data
    WAITFOR DELAY '00:00:10';
    
    PRINT 'Transaction 1 - Rolling back the update';
    
    -- Rollback the transaction
    ROLLBACK TRANSACTION;
    
    PRINT 'Transaction 1 - Rollback complete';
END;
GO

-- Execute the procedure
PRINT 'To demonstrate dirty reads, run this script in one query window';
PRINT 'Then immediately run the 07b_DirtyReads_Transaction2.sql script in another query window';
PRINT 'You can execute this procedure using: EXEC sp_DirtyReads_Transaction1';
GO
