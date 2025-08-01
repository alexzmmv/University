USE University;
GO

-- Transaction 2 for Non-Repeatable Reads - Will read the same data twice and get different results
-- Run this transaction after starting Transaction 1
CREATE OR ALTER PROCEDURE sp_NonRepeatableReads_Transaction2
AS
BEGIN
    PRINT 'Starting Transaction 2 - will demonstrate non-repeatable reads';
    
    -- Set isolation level to READ COMMITTED (default) - allows non-repeatable reads
    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- First read
    PRINT 'Transaction 2 - First read of course data:';
    SELECT Course_ID, Name, Credit_Hours FROM Courses WHERE Course_ID = 1;
    
    -- Wait for Transaction 1 to update and commit
    PRINT 'Transaction 2 - Waiting for Transaction 1 to update and commit...';
    WAITFOR DELAY '00:00:10';
    
    -- Second read - will show different data than the first read (non-repeatable read)
    PRINT 'Transaction 2 - Second read of course data (will show different data):';
    SELECT Course_ID, Name, Credit_Hours FROM Courses WHERE Course_ID = 1;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 2 - Committed';
END;
GO
