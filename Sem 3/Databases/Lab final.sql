create database University;
go
use University;
go
CREATE OR ALTER PROCEDURE UniversityCreate AS
BEGIN

	--create VersionTable
	CREATE TABLE VersionTable (
		VersionID INT PRIMARY KEY identity(1,1),
		Do VARCHAR(100),
		Undo VARCHAR(100)
	);
	
	
    -- Create Buildings table
    CREATE TABLE Buildings (
        Building_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100) NOT NULL,
        Address VARCHAR(200)
    );

    -- Create Rooms table
    CREATE TABLE Rooms (
        Room_ID INT PRIMARY KEY IDENTITY(1,1),
        Building_ID INT NOT NULL,
        Name VARCHAR(100) NOT NULL,
        Capacity INT,
        Floor INT,
        Equipment VARCHAR(200),
        AV_Facilities VARCHAR(200),
        FOREIGN KEY (Building_ID) REFERENCES Buildings(Building_ID)
    );
    -- Create Secretaries table
    CREATE TABLE Secretaries (
        Secretary_ID INT IDENTITY(1,1),
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        Office_Location VARCHAR(100),
		CONSTRAINT PK_Secretary_ID PRIMARY KEY (Secretary_ID,name)
    );
    -- Create Faculties table
    CREATE TABLE Faculties (
        Faculty_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100) NOT NULL,
        Secretary_ID INT NOT NULL UNIQUE,
        Dean VARCHAR(100),
        Established DATE,
        FOREIGN KEY (Secretary_ID) REFERENCES Secretaries(Secretary_ID)
    );

    -- Create Profiles table
    CREATE TABLE Profiles (
        Profile_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100) NOT NULL,
        Faculty_ID INT NOT NULL,
        Duration_Years INT,
        Degree_Type VARCHAR(50),
        FOREIGN KEY (Faculty_ID) REFERENCES Faculties(Faculty_ID)
    );

    -- Create Students table
    CREATE TABLE Students (
        Student_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100) NOT NULL,
        Date_of_Birth DATE,
        Profile_ID INT NOT NULL,
        Email VARCHAR(100),
        Phone VARCHAR(15),
        Enrollment_Date DATE,
        FOREIGN KEY (Profile_ID) REFERENCES Profiles(Profile_ID)
    );

    -- Create Professors table
    CREATE TABLE Professors (
        Professor_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100),
        Faculty_ID INT NOT NULL,
        Email VARCHAR(100),
        Phone VARCHAR(15),
        Office_Location VARCHAR(100),
        FOREIGN KEY (Faculty_ID) REFERENCES Faculties(Faculty_ID)
    );

    -- Create Courses table
    CREATE TABLE Courses (
        Course_ID INT PRIMARY KEY IDENTITY(1,1),
        Code VARCHAR(20) NOT NULL,
        Name VARCHAR(100) NOT NULL,
        Faculty_ID INT NOT NULL,
        Semester INT,
        Credit_Hours INT,
        Description VARCHAR(500),
        FOREIGN KEY (Faculty_ID) REFERENCES Faculties(Faculty_ID)
    );

    -- Create Classes table
    CREATE TABLE Classes (
        Class_ID INT PRIMARY KEY IDENTITY(1,1),
        Course_ID INT NOT NULL,
        Professor_ID INT NOT NULL,
        Room_ID INT NOT NULL,
        Date_Time_Start DATETIME,
        Date_Time_End DATETIME,
        FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID),
        FOREIGN KEY (Professor_ID) REFERENCES Professors(Professor_ID),
        FOREIGN KEY (Room_ID) REFERENCES Rooms(Room_ID)
    );

    -- Create Grades table
    CREATE TABLE Grades (
        Grade_ID INT PRIMARY KEY IDENTITY(1,1),
        Student_ID INT NOT NULL,
        Course_ID INT NOT NULL,
        Grade DECIMAL(3, 2),
        FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
        FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID)
    );

    -- Create Student_Courses table
    CREATE TABLE Student_Courses (
        Student_ID INT NOT NULL,
        Course_ID INT NOT NULL,
        PRIMARY KEY (Student_ID, Course_ID),
        FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID),
        FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID)
    );

    -- Create Course_Rooms table
    CREATE TABLE Course_Rooms (
        Course_ID INT NOT NULL,
        Room_ID INT NOT NULL,
        PRIMARY KEY (Course_ID, Room_ID),
        FOREIGN KEY (Course_ID) REFERENCES Courses(Course_ID),
        FOREIGN KEY (Room_ID) REFERENCES Rooms(Room_ID)
    );

END;
GO


CREATE OR ALTER PROCEDURE [dbo].[InsertInitialData] AS
BEGIN
    -- Insert data into Buildings table
    INSERT INTO Buildings (Name, Address) VALUES 
    ('Central Campus', 'Str. Universitatii 123, Centru'),
    ('Science Building', 'Str. Stiintei 456, Zona de Vest'),
    ('Library', 'Str. Cartilor 789, Zona de Est'),
    ('Sports Complex', 'Str. Sporturilor 101, Zona de Nord'),
    ('Administrative Building', 'Str. Administratiei 202, Aripa Sud');

    -- Insert data into Rooms table
    INSERT INTO Rooms (Building_ID, Name, Capacity, Floor, Equipment, AV_Facilities) VALUES 
    (1, 'Sala 101', 30, 1, 'Banci, Scaune', 'Proiector, Tabla alba'),
    (2, 'Laborator A', 20, 1, 'Calculatoare, Mese de laborator', 'Proiector, Boxe'),
    (3, 'Sala de Conferinte', 50, 2, 'Masa de conferinte, Scaune', 'Televizor, Videoconferinta'),
    (4, 'Sala de Sport', 100, 1, 'Echipamente sportive', 'Sistem de sunet, Proiector'),
    (5, 'Sala de Sedinte Admin', 15, 3, 'Masa, Scaune', 'Proiector, Tabla');

    -- Insert data into Secretaries table
    INSERT INTO Secretaries (Name, Email, Phone, Office_Location) VALUES 
    ('Ana Popescu', 'ana.popescu@universitate.ro', '555-0101', 'Cladirea Administrativa Sala 301'),
    ('Ion Ionescu', 'ion.ionescu@universitate.ro', '555-0102', 'Cladirea Stiintei Sala 102'),
    ('Maria Tudor', 'maria.tudor@universitate.ro', '555-0103', 'Campusul Central Sala 201'),
    ('Andrei Dumitru', 'andrei.dumitru@universitate.ro', '555-0104', 'Biblioteca Sala 101'),
    ('Elena Marin', 'elena.marin@universitate.ro', '555-0105', 'Complexul Sportiv Biroul Central'),
	('Andrei Dumitru', 'andreidumitru1@universitate.ro', '555-0245', 'Complexul Sportiv Biroul Secundar');

    -- Insert data into Faculties table
    INSERT INTO Faculties (Name, Secretary_ID, Dean, Established) VALUES 
    ('Engineering', 1, 'Dr. Mihai Popa', '2001-09-01'),
    ('Sciences', 2, 'Dr. Ioana Georgescu', '1999-01-15'),
    ('Arts', 3, 'Dr. Emilia Negru', '1985-06-20'),
    ('Business', 4, 'Dr. Radu Vasile', '2005-03-10'),
    ('Physical Education', 5, 'Dr. Larisa Rosu', '2010-08-25');

    -- Insert data into Profiles table
    INSERT INTO Profiles (Name, Faculty_ID, Duration_Years, Degree_Type) VALUES 
    ('Informatics', 1, 3, 'Bachelor of Science'),
    ('Mechanical Engineering', 1, 4, 'Bachelor of Engineering'),
    ('Biology', 2, 3, 'Bachelor of Science'),
    ('Visual Arts', 3, 3, 'Bachelor of Arts'),
    ('Business Administration', 4, 3, 'Bachelor of Business Administration');

    -- Insert data into Students table
    INSERT INTO Students (Name, Date_of_Birth, Profile_ID, Email, Phone, Enrollment_Date) VALUES 
    ('Vlad Ionescu', '2002-05-15', 1, 'vlad.ionescu@universitate.ro', '555-0201', '2023-09-01'),
    ('Irina Moldovan', '2003-07-22', 2, 'irina.moldovan@universitate.ro', '555-0202', '2022-09-01'),
    ('Alexandru Pop', '2001-03-30', 3, 'alexandru.pop@universitate.ro', '555-0203', '2024-09-01'),
    ('Simona Vasile', '2002-11-05', 4, 'simona.vasile@universitate.ro', '555-0204', '2023-09-01'),
    ('George Radu', '2003-01-25', 5, 'george.radu@universitate.ro', '555-0205', '2023-09-01'),
	('John Andreson','2005-10-11' ,5,'john.andreson@universitate.ro','432-245','2021-03-01');

    -- Insert data into Professors table
    INSERT INTO Professors (Name, Faculty_ID, Email, Phone, Office_Location) VALUES 
    ('Dr. Daniela Alb', 1, 'daniela.alb@universitate.ro', '555-0301', 'Campus Central Sala 401'),
    ('Dr. Constantin Negru', 2, 'constantin.negru@universitate.ro', '555-0302', 'Cladirea Stiintei Sala 203'),
    ('Dr. Anca Rosu', 3, 'anca.rosu@universitate.ro', '555-0303', 'Cladirea Artelor Sala 301'),
    ('Dr. Cristian Albastru', 4, 'cristian.albastru@universitate.ro', '555-0304', 'Cladirea Business Sala 201'),
    ('Dr. Laura Gri', 5, 'laura.gri@universitate.ro', '555-0305', 'Biroul Complex Sportiv');

    -- Insert data into Courses table
    INSERT INTO Courses (Code, Name, Faculty_ID, Semester, Credit_Hours, Description) VALUES 
    ('INF101', 'Introduction to Informatics', 1, 1, 6, 'Fundamentals of informatics and programming.'),
    ('ENG202', 'Engineering Mechanics', 1, 2, 5, 'Core principles of mechanics in engineering.'),
    ('BIO101', 'Biology Basics', 2, 1, 4, 'Introduction to biology concepts.'),
    ('ART300', 'Modern Art Techniques', 3, 2, 3, 'Exploration of techniques in modern art.'),
    ('BUS101', 'Business Foundations', 4, 1, 3, 'Introduction to business principles.');

    -- Insert data into Classes table
    INSERT INTO Classes (Course_ID, Professor_ID, Room_ID, Date_Time_Start, Date_Time_End) VALUES 
    (1, 1, 1, '2024-01-15 10:00:00', '2024-01-15 11:30:00'),
    (2, 2, 2, '2024-02-01 09:00:00', '2024-02-01 10:30:00'),
    (3, 3, 3, '2024-01-20 14:00:00', '2024-01-20 15:30:00'),
    (4, 4, 4, '2024-01-25 11:00:00', '2024-01-25 12:30:00'),
    (5, 5, 5, '2024-01-30 15:00:00', '2024-01-30 16:30:00');

    -- Insert data into Grades table
    INSERT INTO Grades (Student_ID, Course_ID, Grade) VALUES 
    (1, 1, 8.5),
    (2, 2, 7.7),
    (3, 3, 9.2),
    (4, 4, 6.8),
    (5, 5, 8.00),
	(6,5,9.0);

    -- Insert data into Student_Courses table
    INSERT INTO Student_Courses (Student_ID, Course_ID) VALUES 
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);

    -- Insert data into Course_Rooms table
    INSERT INTO Course_Rooms (Course_ID, Room_ID) VALUES 
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);
END 
go

CREATE OR ALTER PROCEDURE InvalidInsert AS
BEGIN
	INSERT INTO Students(Name,Profile_ID)
	VALUES('ION',999);
END
go

CREATE or ALTER PROCEDURE [dbo].[UpdateEntries] AS
BEGIN
    -- Update Buildings table
    UPDATE Buildings
    SET Name = 'Main Campus Updated', Address = 'Str. Universitatii 123, Centru Updated'
    WHERE Building_ID = 1;

    UPDATE Buildings
    SET Name = 'Science Building Updated', Address = 'Str. Stiintei 456, Zona de Vest Updated'
    WHERE Building_ID = 2;

    -- Update Rooms table
    UPDATE Rooms
    SET Name = 'Updated Sala 101', Capacity = 40
    WHERE Room_ID = 1;

    UPDATE Rooms
    SET Name = 'Updated Laborator A', Capacity = 25
    WHERE Room_ID = 2;

    -- Update Secretaries table
    UPDATE Secretaries
    SET Name = 'Ana Popescu Updated', Email = 'ana.updated@universitate.ro'
    WHERE Secretary_ID = 1;

    UPDATE Secretaries
    SET Name = 'Ion Ionescu Updated', Email = 'ion.updated@universitate.ro'
    WHERE Secretary_ID = 2;

    -- Update Faculties table
    UPDATE Faculties
    SET Name = 'Engineering Updated', Dean = 'Dr. Mihai Updated'
    WHERE Faculty_ID = 1;

    UPDATE Faculties
    SET Name = 'Sciences Updated', Dean = 'Dr. Ioana Updated'
    WHERE Faculty_ID = 2;

    -- Update Profiles table
    UPDATE Profiles
    SET Name = 'Informatics Updated', Duration_Years = 4
    WHERE Profile_ID = 1;

    UPDATE Profiles
    SET Name = 'Mechanical Engineering Updated', Duration_Years = 5
    WHERE Profile_ID = 2;

    -- Update Students table
    UPDATE Students
    SET Name = 'Vlad Ionescu Updated', Email = 'vlad.updated@universitate.ro'
    WHERE Student_ID = 1;

    UPDATE Students
    SET Name = 'Irina Moldovan Updated', Email = 'irina.updated@universitate.ro'
    WHERE Student_ID = 2;

    -- Update Professors table
    UPDATE Professors
    SET Name = 'Dr. Daniela Alb Updated', Email = 'daniela.updated@universitate.ro'
    WHERE Professor_ID = 1;

    UPDATE Professors
    SET Name = 'Dr. Constantin Negru Updated', Email = 'constantin.updated@universitate.ro'
    WHERE Professor_ID = 2;

    -- Update Courses table
    UPDATE Courses
    SET Name = 'Intro to Informatics Updated', Credit_Hours = 7
    WHERE Course_ID = 1;

    UPDATE Courses
    SET Name = 'Engineering Mechanics Updated', Credit_Hours = 6
    WHERE Course_ID = 2;

    -- Update Classes table
    UPDATE Classes
    SET Date_Time_Start = '2024-02-01 08:00:00', Date_Time_End = '2024-02-01 09:30:00'
    WHERE Class_ID = 1;

    UPDATE Classes
    SET Date_Time_Start = '2024-02-05 10:00:00', Date_Time_End = '2024-02-05 11:30:00'
    WHERE Class_ID = 2;

    -- Update Grades table
    UPDATE Grades
    SET Grade = 9.00
    WHERE Grade_ID = 1;

    UPDATE Grades
    SET Grade = 8.50
    WHERE Grade_ID = 2;

    -- Update Student_Courses table
    UPDATE Student_Courses
    SET Course_ID = 2
    WHERE Student_ID = 1;

    UPDATE Student_Courses
    SET Course_ID = 1
    WHERE Student_ID = 2;

    -- Update Course_Rooms table
    UPDATE Course_Rooms
    SET Room_ID = 2
    WHERE Course_ID = 1;

    UPDATE Course_Rooms
    SET Room_ID = 1
    WHERE Course_ID = 2;
END;
GO

go
CREATE or ALTER PROCEDURE DeleteEntries AS
BEGIN
    -- Delete from Course_Rooms table
    DELETE FROM Course_Rooms WHERE Course_ID = 1 AND Room_ID = 1;
    DELETE FROM Course_Rooms WHERE Course_ID = 2 AND Room_ID = 2;

    -- Delete from Student_Courses table
    DELETE FROM Student_Courses WHERE Student_ID = 1 AND Course_ID = 1;
    DELETE FROM Student_Courses WHERE Student_ID = 2 AND Course_ID = 2;

    -- Delete from Grades table
    DELETE FROM Grades WHERE Grade_ID = 1;
    DELETE FROM Grades WHERE Grade_ID = 2;

    -- Delete from Classes table
    DELETE FROM Classes WHERE Class_ID = 1;
    DELETE FROM Classes WHERE Class_ID = 2;

    -- Delete from Courses table
    DELETE FROM Courses WHERE Course_ID = 1;
    DELETE FROM Courses WHERE Course_ID = 2;

    -- Delete from Professors table
    DELETE FROM Professors WHERE Professor_ID = 1;
    DELETE FROM Professors WHERE Professor_ID = 2;

    -- Delete from Students table
    DELETE FROM Students WHERE Student_ID = 1;
    DELETE FROM Students WHERE Student_ID = 2;

    -- Delete from Profiles table
    DELETE FROM Profiles WHERE Profile_ID = 1;
    DELETE FROM Profiles WHERE Profile_ID = 2;

    -- Delete from Faculties table
    DELETE FROM Faculties WHERE Faculty_ID = 1;
    DELETE FROM Faculties WHERE Faculty_ID = 2;

    -- Delete from Secretaries table
    DELETE FROM Secretaries WHERE Secretary_ID = 1;
    DELETE FROM Secretaries WHERE Secretary_ID = 2;

    -- Delete from Rooms table
    DELETE FROM Rooms WHERE Room_ID = 1;
    DELETE FROM Rooms WHERE Room_ID = 2;

    -- Delete from Buildings table
    DELETE FROM Buildings WHERE Building_ID = 1;
    DELETE FROM Buildings WHERE Building_ID = 2;
END;
GO

go 
CREATE OR ALTER PROCEDURE UnionQueries AS
BEGIN
    -- Query 1: Union using UNION ALL
    SELECT Name FROM Students WHERE Enrollment_Date >= '2023-01-01'
    UNION ALL
    SELECT Name FROM Professors WHERE Email LIKE '%@universitate.ro';

    -- Query 2: Union using OR
    SELECT Name FROM Secretaries WHERE Name LIKE 'A%'
    UNION
    SELECT Name FROM Faculties WHERE Established < '2000-01-01';
END
GO

CREATE OR ALTER PROCEDURE IntersectionQueries AS
BEGIN
    -- Query 1: Intersection using INTERSECT
    SELECT Name FROM Students WHERE Enrollment_Date >= '2023-01-01'
    INTERSECT
    SELECT Name FROM Professors WHERE Email LIKE '%@universitate.ro';

    -- Query 2: Intersection using IN
    SELECT Name FROM Secretaries WHERE Secretary_ID IN (SELECT Secretary_ID FROM Faculties);
END
GO

CREATE OR ALTER PROCEDURE DifferenceQueries AS
BEGIN
    -- Query 1: Difference using EXCEPT
    SELECT Name FROM Students
    EXCEPT
    SELECT Name FROM Professors;

    -- Query 2: Difference using NOT IN
    SELECT Name FROM Courses WHERE Faculty_ID NOT IN (SELECT Faculty_ID FROM Faculties WHERE Dean = 'Dr. Mihai Popa');
END
GO


CREATE OR ALTER PROCEDURE JoinQueries AS
BEGIN
    -- INNER JOIN: Join at least 3 tables
    SELECT Students.Name AS Student_Name, Profiles.Name AS Profile_Name, Faculties.Name AS Faculty_Name
    FROM Students
    INNER JOIN Profiles ON Students.Profile_ID = Profiles.Profile_ID
    INNER JOIN Faculties ON Profiles.Faculty_ID = Faculties.Faculty_ID;

    -- LEFT JOIN: Join Students and Grades
    SELECT Students.Name AS Student_Name, Grades.Grade
    FROM Students
    LEFT JOIN Grades ON Students.Student_ID = Grades.Student_ID;

    -- RIGHT JOIN: Join Professors and Courses
    SELECT Professors.Name AS Professor_Name, Courses.Name AS Course_Name
    FROM Professors
    RIGHT JOIN Courses ON Professors.Faculty_ID = Courses.Faculty_ID;

    -- FULL JOIN: Join Classes and Rooms
    SELECT Classes.Class_ID, Rooms.Name AS Room_Name
    FROM Classes
    FULL JOIN Rooms ON Classes.Room_ID = Rooms.Room_ID;
END
GO

CREATE OR ALTER PROCEDURE SubqueryInWhere AS
BEGIN
    -- Query 1: Using IN with a subquery
    SELECT Name FROM Students 
    WHERE Profile_ID IN (SELECT Profile_ID FROM Profiles WHERE Duration_Years > 3);

	select * from Students
	select  * from Profiles

    -- Query 2: Nested subquery in WHERE clause
    SELECT Name FROM Professors 
    WHERE Faculty_ID IN (SELECT Faculty_ID FROM Faculties WHERE Secretary_ID IN (SELECT Secretary_ID FROM Secretaries));
END
GO

CREATE OR ALTER PROCEDURE ExistsQueries AS
BEGIN
    -- Query 1: Using EXISTS
    SELECT Name FROM Students
    WHERE EXISTS (SELECT 1 FROM Grades WHERE Grades.Student_ID = Students.Student_ID AND Grades.Grade < 5);

    -- Query 2: Nested EXISTS
    SELECT Name FROM Professors
    WHERE EXISTS (SELECT 1 FROM Courses WHERE Courses.Faculty_ID = Professors.Faculty_ID AND EXISTS (SELECT 1 FROM Classes  WHERE Classes.Course_ID = Courses.Course_ID));
END
GO

CREATE OR ALTER PROCEDURE SubqueryInFrom AS
BEGIN
    -- Query 1: Subquery in FROM clause for counting professors by faculty
    SELECT A.Faculty_ID, A.Faculty_Count
    FROM (SELECT Faculty_ID, COUNT(*) AS Faculty_Count 
          FROM Professors 
          GROUP BY Faculty_ID) A;

    -- Query 2: Subquery in FROM clause for counting courses by student
    SELECT B.Student_ID, B.Course_Count
    FROM (SELECT Student_ID, COUNT(*) AS Course_Count 
          FROM Student_Courses 
          GROUP BY Student_ID) B;
END
GO




CREATE OR ALTER PROCEDURE GroupByQueries AS
BEGIN
	-- Query 1: GROUP BY with COUNT of students by Profile
	SELECT Profiles.Profile_ID, COUNT(Students.Student_ID) AS Student_Count
	FROM Students
	JOIN Profiles ON Students.Profile_ID = Profiles.Profile_ID
	GROUP BY Profiles.Profile_ID;


    -- Query 2: GROUP BY with HAVING for average grade by Profile
    SELECT Profiles.Profile_ID, AVG(Grades.Grade) AS Average_Grade
    FROM Grades
    JOIN Students ON Grades.Student_ID = Students.Student_ID
    JOIN Profiles ON Students.Profile_ID= Profiles.Profile_ID
    GROUP BY Profiles.Profile_ID
    HAVING AVG(Grades.Grade) >= 8;

    -- Query 3: GROUP BY with a subquery in HAVING for profiles with student count above average
    SELECT Profile_ID, COUNT(*) AS Student_Count
    FROM Students
    GROUP BY Profile_ID
    HAVING COUNT(*) > (SELECT AVG(Student_Count) 
                       FROM (SELECT Profile_ID, COUNT(*) AS Student_Count 
                             FROM Students 
                             GROUP BY Profile_ID) AS Subquery);

    -- Query 4: GROUP BY with SUM of total credit hours by faculty
    SELECT Courses.Faculty_ID, SUM(Courses.Credit_Hours) AS Total_Credits
    FROM Courses
    GROUP BY Courses.Faculty_ID;
END
GO
--
CREATE OR ALTER PROCEDURE FinalQueries AS
BEGIN
    
	-- Query 1: List all Students with their respective Profiles
    SELECT Students.Name AS Student_Name, Profiles.Name AS Profile_Name
    FROM Students
    JOIN Profiles ON Students.Profile_ID = Profiles.Profile_ID;

    -- Query 2: List all Professors who teach courses in a specific Faculty
    SELECT Professors.Name AS Professor_Name, Faculties.Name AS Faculty_Name
    FROM Professors
    JOIN Faculties ON Professors.Faculty_ID = Faculties.Faculty_ID
    WHERE Faculties.Name = 'Engineering';

    -- Query 3: Total Grades of Students per Profile
    SELECT Profiles.Name AS Profile_Name, SUM(Grades.Grade) AS Total_Grades
    FROM Profiles 
    JOIN Students ON Profiles.Profile_ID = Students.Profile_ID
    JOIN Grades ON Students.Student_ID = Grades.Student_ID
    GROUP BY Profiles.Name;

    -- Query 4: Average Credit Hours of Courses in each Faculty
    SELECT Faculties.Name AS Faculty_Name, AVG(Courses.Credit_Hours) AS Average_Credit_Hours
    FROM Faculties 
    JOIN Courses ON Faculties.Faculty_ID = Courses.Faculty_ID
    GROUP BY Faculties.Name;
END
GO


CREATE OR ALTER PROCEDURE AnyAllQueries AS
BEGIN
    -- Query 1: ANY with subquery
    SELECT Name FROM Students
    WHERE Enrollment_Date > ALL (SELECT Enrollment_Date FROM Students WHERE Date_of_Birth < '2000-01-01');

    -- Query 2: ANY with aggregation operator
    SELECT Name FROM Professors
    WHERE Faculty_ID = ANY (SELECT Faculty_ID FROM Faculties WHERE Established < '2000-01-01');

    -- Query 3: NOT IN with subquery
    SELECT Name FROM Courses
    WHERE Faculty_ID NOT IN (SELECT Faculty_ID FROM Faculties WHERE Dean = 'Dr. Mihai Popa');

    -- Query 4: NOT IN with aggregation operator
    SELECT Name FROM Students
    WHERE Profile_ID NOT IN (SELECT Profile_ID FROM Profiles WHERE Duration_Years > ALL (SELECT Duration_Years FROM Profiles));
END
GO




--a. modify the type of a column;
CREATE OR ALTER PROCEDURE GradeToFloat AS
BEGIN
	ALTER TABLE Grades
	ALTER COLUMN GRADE FLOAT;

END;
GO

CREATE OR ALTER PROCEDURE GradeToDecimal AS
BEGIN
	ALTER TABLE Grades
	ALTER COLUMN GRADE DECIMAL(3,2);
END;
GO

--b. add / remove a column;
CREATE OR ALTER PROCEDURE AddAgeStudents AS
BEGIN
    ALTER TABLE Students
    ADD Age INT;
END;
GO

CREATE OR ALTER PROCEDURE RemoveAgeStudents AS
BEGIN
    ALTER TABLE Students
    DROP COLUMN Age;
END;
GO

--c. add / remove a DEFAULT constraint;
CREATE OR ALTER PROCEDURE AddDefaultEmail AS
BEGIN
    ALTER TABLE Students
    ADD CONSTRAINT DF_Students_Email DEFAULT ''
    FOR Email;
END;
GO

CREATE OR ALTER PROCEDURE RemoveDefaultEmail AS
BEGIN
    ALTER TABLE Students
    DROP CONSTRAINT DF_Students_Email;
END;
GO

--e. add / remove a candidate key;
CREATE OR ALTER PROCEDURE AddStudentsCandidateKey AS
BEGIN
    ALTER TABLE Students
    ADD CONSTRAINT AK_Students_Email UNIQUE (Email);
END;
GO

CREATE OR ALTER PROCEDURE RemoveStudentsCandidateKey AS
BEGIN
    ALTER TABLE Students
    DROP CONSTRAINT AK_Students_Email;
END;
GO

--f. add / remove a foreign key;
CREATE OR ALTER PROCEDURE AddStudentsProfileForeignKey AS
BEGIN
    ALTER TABLE Students
    ADD CONSTRAINT FK_Students_Profiles FOREIGN KEY (Profile_ID) REFERENCES Profiles(Profile_ID);

END;
GO

CREATE OR ALTER PROCEDURE RemoveStudentsProfileForeignKey AS
BEGIN
    ALTER TABLE Students
    DROP CONSTRAINT FK_Students_Profiles;
END;
GO

--g. create / drop a table.
CREATE OR ALTER PROCEDURE CreateTestTable AS
BEGIN
    CREATE TABLE TestTable (
        Test_ID INT NOT NULL,
        Test_Name VARCHAR(100)
    );
END;
GO

CREATE OR ALTER PROCEDURE DropTestTable AS
BEGIN
    DROP TABLE TestTable;
END;
GO

--d. add / remove a primary key;-dosen't work
CREATE OR ALTER PROCEDURE AddTestTablePrimaryKey AS
	 BEGIN
      ALTER TABLE TestTable
        ADD CONSTRAINT PK_TestTable PRIMARY KEY (Test_ID);
    END
GO

CREATE OR ALTER PROCEDURE RemoveTestTablePrimaryKey AS
	 BEGIN
		 ALTER TABLE TestTable
        DROP CONSTRAINT PK_TestTable;
	END
 GO

drop table VersioningTable;
-- Versioning Table
CREATE TABLE VersioningTable (
    Current_Procedure NVARCHAR(50),
    Previous_Procedure NVARCHAR(50),
    versionTO INT
);

-- Insert versioning procedures
INSERT INTO VersioningTable (Current_Procedure, Previous_Procedure, versionTO) VALUES
('GradeToFloat', 'GadeToDecimal', 1),
('AddAgeStudents', 'RemoveAgeStudents', 2),
('AddDefaultEmail', 'RemoveDefaultEmail', 3),
('AddStudentsCandidateKey', 'RemoveStudentsCandidateKey', 4),
('AddStudentsProfileForeignKey', 'RemoveStudentsProfileForeignKey', 5),
('CreateTestTable', 'DropTestTable', 6),
('AddTestTablePrimaryKey','RemoveTestTablePrimaryKey',7);

-- Current Version Table
DROP TABLE IF EXISTS CurrentVersion;
CREATE TABLE CurrentVersion (
    currentVersion INT DEFAULT 0
);

INSERT INTO CurrentVersion VALUES (0);
GO

-- Version Management Procedure
CREATE OR ALTER PROCEDURE goToVersion(@version INT)
AS
BEGIN
    DECLARE @currentVersion INT;
    DECLARE @currentProcedure NVARCHAR(50);

    IF @version < 0 OR @version > 7
    BEGIN
        RAISERROR('Invalid version! Please choose a version between 0 and 7.', 17, 1);
        RETURN;
    END

    SET @currentVersion = (SELECT currentVersion FROM CurrentVersion);

    IF @version = @currentVersion
    BEGIN
        PRINT 'We are already on this version!';
        RETURN;
    END

    IF @currentVersion < @version
    BEGIN
        WHILE @currentVersion < @version
        BEGIN
            PRINT'Upgrading to version ' + CAST(@currentVersion + 1 AS NVARCHAR(10));
            SET @currentProcedure = (SELECT Current_Procedure FROM VersioningTable WHERE versionTO = @currentVersion + 1);
            EXEC(@currentProcedure);
            SET @currentVersion = @currentVersion + 1;
        END
    END

    IF @currentVersion > @version
    BEGIN
        WHILE @currentVersion > @version
        BEGIN
            PRINT 'Downgrading to version ' + CAST(@currentVersion - 1 AS NVARCHAR(10));
            SET @currentProcedure = (SELECT Previous_Procedure FROM VersioningTable WHERE versionTO = @currentVersion);
            EXEC(@currentProcedure);
            SET @currentVersion = @currentVersion - 1;
        END
    END

    UPDATE CurrentVersion
    SET currentVersion = @currentVersion;

    PRINT 'Current version updated!';
    PRINT 'Now at version: ' + CAST(@currentVersion AS NVARCHAR(10));
END;
GO

exec goToVersion 0;
select * from Students;
GO

CREATE OR ALTER VIEW View_1 AS
SELECT
	S.Name,
	S.Email,
	S.Office_Location
FROM Secretaries S
GO

CREATE OR ALTER VIEW View_2 AS
	SELECT 
    R.Name AS RoomName,
    B.Name AS BuildingName,
    R.Capacity,
    R.Floor
FROM Buildings B
INNER JOIN Rooms R ON B.Building_ID = R.Building_ID;

GO
CREATE OR ALTER VIEW View_3 AS
SELECT 
    B.Building_ID,
    B.Name AS BuildingName,
    COUNT(R.Room_ID) AS TotalRooms,
    SUM(R.Capacity) AS TotalCapacity
FROM Buildings B
LEFT JOIN Rooms R ON B.Building_ID = R.Building_ID
GROUP BY B.Building_ID, B.Name;
GO

CREATE OR ALTER PROCEDURE InsertIntoBuilding(@RecNum INT) AS
BEGIN
    DECLARE @Counter INT = 1;

    WHILE @Counter <= @RecNum
    BEGIN
        INSERT INTO Buildings (Name, Address)
        VALUES 
            (CONCAT('Building', @Counter), CONCAT('Address', @Counter));
        
        SET @Counter = @Counter + 1;
    END
END
GO

CREATE OR ALTER PROCEDURE DeleteFromBuilding(@RecNum INT) AS
BEGIN
	DELETE FROM Buildings
	WHERE Building_ID in(
	select TOP(@RecNum) Building_ID
	FROM Buildings
	ORDER BY Building_ID DESC
	)
END
GO

CREATE OR ALTER PROCEDURE InsertIntoRooms(@RecNum INT,@IdToAttach INT) AS
BEGIN
    DECLARE @Counter INT = 1;
    WHILE @Counter <= @RecNum
    BEGIN
        INSERT INTO Rooms (Name, Building_ID,Capacity,Floor,Equipment,AV_Facilities)
        VALUES 
            (CONCAT('RoomTestTest', @Counter), @IdToAttach,@Counter,RAND(),CONCAT('Equipment', @Counter),CONCAT('AV_Facilities', @Counter));
        
        SET @Counter = @Counter + 1;
    END
END
GO

CREATE OR ALTER PROCEDURE DeleteFromRooms(@RecNum INT) AS
BEGIN
	DELETE FROM Rooms
	WHERE Room_ID in(
	select TOP(@RecNum) Room_ID
	FROM Rooms
    WHERE Name like 'RoomTestTest%'
	ORDER BY Room_ID DESC
	)
    if @@ROWCOUNT < @RecNum
        print 'There were less than ' + CAST(@RecNum AS NVARCHAR(10)) + ' records to delete';
    
END
GO


CREATE OR ALTER PROCEDURE InsertIntoSecretaries(@RecNum INT) AS
BEGIN
    DECLARE @Counter INT = 1;

    WHILE @Counter <= @RecNum
    BEGIN
        INSERT INTO Secretaries(Name,Email,Office_Location,Phone)
        VALUES 
            (CONCAT('TestSecretary', @Counter),
			CONCAT('TestSecretary', @Counter,'@gmail.com'),
			CONCAT('Street num ', @Counter),
			CONCAT('+34.', @Counter)
			);
        
        SET @Counter = @Counter + 1;
    END
END
GO

CREATE OR ALTER PROCEDURE DeleteFromSecretaries(@RecNum INT) AS
BEGIN
	DELETE FROM Secretaries
	WHERE Secretary_ID in(
	select TOP(@RecNum) Secretary_ID
	FROM Secretaries
	ORDER BY Secretary_ID DESC
	)
END
GO

--run DB_CSEn_Script_lab4

INSERT INTO Tables(Name) VALUES 
	('Buildings'),
	('Rooms'),
	('Secretaries');
select * from Tables;

INSERT INTO Views(Name) VALUES 
	('View_1'),
	('View_2'),
	('View_3');
select * from Views;

INSERT INTO Tests(Name) VALUES
	('insert/view_1/delete-Secretaries'),
	('insert/view_2/delete-Rooms'),
	('insert/view_3/delete-Rooms&Buildings');

select * from Tests;

INSERT INTO TestViews(TestID,ViewID) VALUES
	(1,1),
	(2,2),
	(3,3);

select * from TestViews;

INSERT INTO TestTables(TestID,TableID,NoOfRows,Position) VALUES
	(1,3,2000,3),
	(2,2,1520,1),
	(3,2,500,1);


select * from Tables;
select * from TestTables;
select * from Tests;
select * from TestViews;
select * from Views;
select * from TestTables;

select * from TestRunTables;
select * from TestRunViews;
select * from TestRuns;


INSERT INTO TestRuns (Description) VALUES 
	('insert/view_1/delete-Secretaries'),
	('insert/view_2/delete-Rooms'),
	('insert/view_3/delete-Buildings');



GO
CREATE OR ALTER PROCEDURE PerformTestRun
    @TableId INT,
    @ViewId INT,
    @OperationType INT, -- 1: Insert/Delete, 2: View, 3: Insert/View/Delete
    @NoOfRows INT
AS
BEGIN
    DECLARE @StartAt DATETIME;
    DECLARE @EndAt DATETIME;
    DECLARE @MaxBuildingId INT;
    DECLARE @TableName NVARCHAR(255);
    DECLARE @ViewName NVARCHAR(255);
    DECLARE @MaxTestRunID INT;

    SELECT @TableName = T.name FROM Tables T WHERE TableID = @TableId;
    SELECT @ViewName = V.name FROM Views V WHERE ViewID = @ViewId;

    SET @StartAt = GETDATE();

    IF @OperationType = 1 OR @OperationType = 3
    BEGIN
        IF @TableId = 1
            EXEC InsertIntoSecretaries @NoOfRows;
        ELSE IF @TableId = 2
            EXEC InsertIntoRooms @NoOfRows, @TableId;
        ELSE IF @TableId = 3
            EXEC InsertIntoBuilding @NoOfRows;

        IF @OperationType = 3
        BEGIN
            IF @ViewId = 1
                SELECT * FROM View_1;
            ELSE IF @ViewId = 2
                SELECT * FROM View_2;
            ELSE IF @ViewId = 3
                SELECT * FROM View_3;
        END

        IF @TableId = 1
            EXEC DeleteFromSecretaries @NoOfRows;
        ELSE IF @TableId = 2
            EXEC DeleteFromRooms @NoOfRows;
        ELSE IF @TableId = 3
            EXEC DeleteFromBuilding @NoOfRows;
    END

    IF @OperationType = 2
    BEGIN
        IF @ViewId = 1
            SELECT * FROM View_1;
        ELSE IF @ViewId = 2
            SELECT * FROM View_2;
        ELSE IF @ViewId = 3
            SELECT * FROM View_3;
    END

    SET @EndAt = GETDATE();

    IF @OperationType = 1
    BEGIN
        INSERT INTO TestRuns (Description, StartAt, EndAt)
        VALUES (CONCAT('Insert/Delete: ', @TableName, ':', @NoOfRows), @StartAt, @EndAt);

        SELECT @MaxTestRunID = MAX(TestRunID) FROM TestRuns;

        INSERT INTO TestRunTables (TestRunID, StartAt, EndAt)
        VALUES (@MaxTestRunID, @StartAt, @EndAt);
    END
    ELSE IF @OperationType = 2
    BEGIN
        INSERT INTO TestRuns (Description, StartAt, EndAt)
        VALUES (@ViewName, @StartAt, @EndAt);

        SELECT @MaxTestRunID = MAX(TestRunID) FROM TestRuns;

        INSERT INTO TestRunViews (TestRunID, StartAt, EndAt)
        VALUES (@MaxTestRunID, @StartAt, @EndAt);
    END
    ELSE IF @OperationType = 3
    BEGIN
        INSERT INTO TestRuns (Description, StartAt, EndAt)
        VALUES (CONCAT('Insert/', @ViewName, '/Delete: ', @TableName, ':', @NoOfRows), @StartAt, @EndAt);

        SELECT @MaxTestRunID = MAX(TestRunID) FROM TestRuns;

        INSERT INTO TestRunTables (TestRunID,TableID, StartAt, EndAt)
        VALUES (@MaxTestRunID,@TableId, @StartAt, @EndAt);

        INSERT INTO TestRunViews (TestRunID,ViewID,StartAt, EndAt)
        VALUES (@MaxTestRunID, @ViewId,@StartAt, @EndAt);
    END

END
GO

exec PerformTestRun 3,1,3,100;

SELECT 
    tr.*, 
    DATEDIFF(MILLISECOND, tr.StartAt, tr.EndAt) AS DurationInMiliSeconds
FROM 
    TestRuns tr;

GO
