USE University;
GO

-- Transaction 2 for Phantom Reads - Will do the same query twice and get different row counts
-- Run this transaction after starting Transaction 1
CREATE OR ALTER PROCEDURE sp_PhantomReads_Transaction2
AS
BEGIN
    PRINT 'Starting Transaction 2 - will demonstrate phantom reads';
    
    -- Set isolation level to REPEATABLE READ - prevents non-repeatable reads but allows phantom reads
    SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- First read - count and list all courses
    PRINT 'Transaction 2 - First count and list of courses:';
    SELECT COUNT(*) AS CourseCount FROM Courses;
    SELECT Course_ID, Code, Name FROM Courses;
    
    -- Wait for Transaction 1 to insert and commit
    PRINT 'Transaction 2 - Waiting for Transaction 1 to insert and commit...';
    WAITFOR DELAY '00:00:10';
    
    -- Second read - will show different row count than the first read (phantom read)
    PRINT 'Transaction 2 - Second count and list of courses (will show new rows):';
    SELECT COUNT(*) AS CourseCount FROM Courses;
    SELECT Course_ID, Code, Name FROM Courses;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 2 - Committed';
END;
GO
