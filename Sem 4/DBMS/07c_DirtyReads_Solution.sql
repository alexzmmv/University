USE University;
GO

-- Solution for Dirty Reads - Use READ COMMITTED isolation level
-- Run this after starting Transaction 1
CREATE OR ALTER PROCEDURE sp_DirtyReads_Solution
AS
BEGIN
    PRINT 'Starting Dirty Reads Solution - will prevent dirty reads';
    
    -- Set isolation level to READ COMMITTED to prevent dirty reads
    SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- First read - will show original data
    PRINT 'Solution - First read, showing original course name:';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Wait a bit to allow Transaction 1 to update the data
    WAITFOR DELAY '00:00:05';
    
    -- Second read - will NOT show the uncommitted update from Transaction 1 
    -- Instead, it will wait until Transaction 1 completes (rolls back in this case)
    PRINT 'Solution - Second read, will NOT show uncommitted data:';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Wait for Transaction 1 to rollback
    WAITFOR DELAY '00:00:10';
    
    -- Third read - will show data after Transaction 1 rollback
    PRINT 'Solution - Third read, after Transaction 1 rollback:';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Solution - Complete. No dirty reads occurred. READ COMMITTED prevented reading uncommitted data.';
END;
GO

-- Execute the procedure
PRINT 'To demonstrate the solution to dirty reads:';
PRINT '1. First run 07a_DirtyReads_Transaction1.sql in one query window';
PRINT '2. Then immediately run this script in another query window';
PRINT 'You can execute this procedure using: EXEC sp_DirtyReads_Solution';
GO
    
    -- Third read - will show data after Transaction 1 rollback
    PRINT 'Solution - Third read, after Transaction 1 rollback:';
    SELECT Course_ID, Name FROM Courses WHERE Course_ID = 1;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Solution - Committed';
END;
GO
