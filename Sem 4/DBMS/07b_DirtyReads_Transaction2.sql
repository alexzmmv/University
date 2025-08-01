USE University;
GO

-- Transaction 2 for Dirty Reads - Will read uncommitted data
-- Run this transaction after starting Transaction 1
CREATE OR ALTER PROCEDURE sp_DirtyReads_Transaction2
AS
BEGIN
    PRINT 'Starting Transaction 2 - will demonstrate dirty reads';
    
    -- Set isolation level to READ UNCOMMITTED to allow dirty reads
    SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    
    -- Begin the transaction
    BEGIN TRANSACTION;
    
    -- First read - will show original data
    PRINT 'Transaction 2 - First read, showing original course name:';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Wait a bit to allow Transaction 1 to update the data
    WAITFOR DELAY '00:00:05';
    
    -- Second read - will show the uncommitted update from Transaction 1
    PRINT 'Transaction 2 - Second read, showing uncommitted course name (dirty read):';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Wait for Transaction 1 to rollback
    WAITFOR DELAY '00:00:10';
    
    -- Third read - will show data after Transaction 1 rollback
    PRINT 'Transaction 2 - Third read, after Transaction 1 rollback:';
    SELECT Course_ID, Code, Name FROM Courses WHERE Course_ID = 1 OR Code = 'TEST001';
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 2 - Complete. The second read showed a dirty read of uncommitted data.';
END;
GO

-- Execute the procedure
PRINT 'To demonstrate dirty reads, first run 07a_DirtyReads_Transaction1.sql in one query window';
PRINT 'Then immediately run this script in another query window';
PRINT 'You can execute this procedure using: EXEC sp_DirtyReads_Transaction2';
GO
    
    -- Third read - will show data after Transaction 1 rollback
    PRINT 'Transaction 2 - Third read, after Transaction 1 rollback:';
    SELECT Course_ID, Name FROM Courses WHERE Course_ID = 1;
    
    -- Commit the transaction
    COMMIT TRANSACTION;
    
    PRINT 'Transaction 2 - Committed';
END;
GO
