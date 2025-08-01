USE University;
GO

-- Transaction 1 for Non-Repeatable Reads - Will update a course during another transaction's read
-- Run this transaction first
CREATE OR ALTER PROCEDURE sp_NonRepeatableReads_Transaction1
AS
BEGIN
    PRINT 'Starting Transaction 1 - will update course data while Transaction 2 is reading';
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- Wait to allow Transaction 2 to do its first read
    PRINT 'Transaction 1 - Waiting for Transaction 2 to do first read...';
    WAITFOR DELAY '00:00:05';
    
    -- Update a course
    PRINT 'Transaction 1 - Updating course credit hours...';
    UPDATE Courses 
    SET Credit_Hours = Credit_Hours + 2
    WHERE Course_ID = 1;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 1 - Committed update';
END;
GO
