USE University;
GO

-- Solution for Non-Repeatable Reads - Use REPEATABLE READ isolation level
-- Run this after starting Transaction 1
CREATE OR ALTER PROCEDURE sp_NonRepeatableReads_Solution
AS
BEGIN
    PRINT 'Starting Non-Repeatable Reads Solution - will prevent non-repeatable reads';
    
    -- Set isolation level to REPEATABLE READ to prevent non-repeatable reads
    SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- First read
    PRINT 'Solution - First read of course data:';
    SELECT Course_ID, Name, Credit_Hours FROM Courses WHERE Course_ID = 1;
    
    -- Wait for Transaction 1 to try to update and commit
    PRINT 'Solution - Waiting while Transaction 1 tries to update...';
    WAITFOR DELAY '00:00:10';
    
    -- Second read - will show the same data as the first read
    -- Transaction 1's update will be blocked until this transaction completes
    PRINT 'Solution - Second read of course data (will show the same data):';
    SELECT Course_ID, Name, Credit_Hours FROM Courses WHERE Course_ID = 1;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Solution - Committed';
    
    -- Show the data after both transactions have completed
    PRINT 'Solution - Data after both transactions completed:';
    SELECT Course_ID, Name, Credit_Hours FROM Courses WHERE Course_ID = 1;
END;
GO
