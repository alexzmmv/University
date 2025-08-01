go
USE University;
GO

-- Validate if a string starts with uppercase
CREATE OR ALTER FUNCTION uf_ValidateFirstLetterUppercase (@str VARCHAR(100))
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@str IS NOT NULL AND LEN(@str) > 0 AND ASCII(LEFT(@str, 1)) BETWEEN ASCII('A') AND ASCII('Z'))
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate email format
CREATE OR ALTER FUNCTION uf_ValidateEmail (@email VARCHAR(100))
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@email IS NOT NULL AND @email LIKE '%_@_%._%' AND @email NOT LIKE '%@%@%')
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate phone number format (accepts format: +XX-XXX-XXX-XXXX or XXXXXXXXXX)                                
CREATE OR ALTER FUNCTION uf_ValidatePhone (@phone VARCHAR(15))
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@phone IS NOT NULL AND 
        (
            (@phone LIKE '+[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]') OR
            (@phone LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
        )
       )
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate date - must be a date in the past
CREATE OR ALTER FUNCTION uf_ValidatePastDate (@date DATE)
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@date IS NOT NULL AND @date <= GETDATE())
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate semester (must be between 1 and 8)
CREATE OR ALTER FUNCTION uf_ValidateSemester (@semester INT)
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@semester IS NOT NULL AND @semester BETWEEN 1 AND 8)
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate credit hours (must be between 1 and 6)
CREATE OR ALTER FUNCTION uf_ValidateCreditHours (@creditHours INT)
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@creditHours IS NOT NULL AND @creditHours BETWEEN 1 AND 6)
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate degree type
CREATE OR ALTER FUNCTION uf_ValidateDegreeType (@degreeType VARCHAR(50))
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@degreeType IN ('Bachelor', 'Master', 'PhD', 'Associate'))
        SET @return = 1;
    
    RETURN @return;
END;
GO

-- Validate course code format (accepts format: XXX#### - 3 letters followed by 4 digits)
CREATE OR ALTER FUNCTION uf_ValidateCourseCode (@code VARCHAR(20))
RETURNS BIT
AS
BEGIN
    DECLARE @return BIT = 0;
    
    IF (@code IS NOT NULL AND @code LIKE '[A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9]')
        SET @return = 1;
    
    RETURN @return;
END;
GO

print 'Validation functions created successfully';



