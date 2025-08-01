USE University;
GO

-- Transaction 1 for Phantom Reads - Will insert a new course during another transaction's read
-- Run this transaction first
CREATE OR ALTER PROCEDURE sp_PhantomReads_Transaction1
AS
BEGIN
    PRINT 'Starting Transaction 1 - will insert a new course while Transaction 2 is reading';
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- Wait to allow Transaction 2 to do its first read
    PRINT 'Transaction 1 - Waiting for Transaction 2 to do first read...';
    WAITFOR DELAY '00:00:05';
    
    -- Insert a new course in the range that Transaction 2 is querying
    PRINT 'Transaction 1 - Inserting new course...';
    INSERT INTO Courses (Code, Name, Faculty_ID, Semester, Credit_Hours, Description)
    VALUES ('CSE9999', 'Phantom Course', 1, 1, 3, 'This course appears during a transaction');
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 1 - Committed insert';
END;
GO
