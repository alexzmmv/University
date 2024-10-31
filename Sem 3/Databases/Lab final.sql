/****** Object:  StoredProcedure [dbo].[UniversityCreate]    Script Date: 30/10/2024 08:44:11 ******/
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[UniversityCreate] AS
BEGIN
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
        Secretary_ID INT PRIMARY KEY IDENTITY(1,1),
        Name VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        Office_Location VARCHAR(100)
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


ALTER PROCEDURE [dbo].[InsertInitialData] AS
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
    ('George Radu', '2003-01-25', 5, 'george.radu@universitate.ro', '555-0205', '2023-09-01');

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
    (1, 1, 8.50),
    (2, 2, 7.75),
    (3, 3, 9.20),
    (4, 4, 6.80),
    (5, 5, 8.00);

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

ALTER PROCEDURE InvalidInsert AS
BEGIN
	INSERT INTO Students(Name,Profile_ID)
	VALUES('ION',999);
END
go

ALTER PROCEDURE UpdateUniversityData
AS
BEGIN
    -- Update Buildings table
    UPDATE Buildings
    SET Address = 'Str. Universitatii 999, Centru'
    WHERE Name = 'Central Campus' AND Address = 'Str. Universitatii 123, Centru';

    -- Update Secretaries table
    UPDATE Secretaries
    SET Email = 'andrei.dumitru2@university.ro'
    WHERE Name = 'Andrei Dumitru' AND Secretary_ID NOT IN (SELECT Secretary_ID FROM Faculties);

    -- Update Rooms table
    UPDATE Rooms
    SET AV_Facilities = 'Advanced Sound System'
    WHERE Floor IN (1, 2) AND Capacity BETWEEN 20 AND 100;
END;
go

go
ALTER PROCEDURE DeleteData AS
BEGIN
    -- Delete data from Rooms table
    DELETE FROM Rooms 
    WHERE Room_ID IN (SELECT Room_ID FROM Rooms WHERE Capacity < 15);

    -- Delete data from Students table
    DELETE FROM Students 
    WHERE Profile_ID NOT IN (SELECT Profile_ID FROM Profiles WHERE Degree_Type LIKE '%Bachelor%');
END
GO
ALTER PROCEDURE UnionQueries AS
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

ALTER PROCEDURE IntersectionQueries AS
BEGIN
    -- Query 1: Intersection using INTERSECT
    SELECT Name FROM Students WHERE Enrollment_Date >= '2023-01-01'
    INTERSECT
    SELECT Name FROM Professors WHERE Email LIKE '%@universitate.ro';

    -- Query 2: Intersection using IN
    SELECT Name FROM Secretaries WHERE Secretary_ID IN (SELECT Secretary_ID FROM Faculties);
END
GO

ALTER PROCEDURE DifferenceQueries AS
BEGIN
    -- Query 1: Difference using EXCEPT
    SELECT Name FROM Students
    EXCEPT
    SELECT Name FROM Professors;

    -- Query 2: Difference using NOT IN
    SELECT Name FROM Courses WHERE Faculty_ID NOT IN (SELECT Faculty_ID FROM Faculties WHERE Dean = 'Dr. Mihai Popa');
END
GO


ALTER PROCEDURE JoinQueries AS
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

ALTER PROCEDURE SubqueryInWhere AS
BEGIN
    -- Query 1: Using IN with a subquery
    SELECT Name FROM Students 
    WHERE Profile_ID IN (SELECT Profile_ID FROM Profiles WHERE Duration_Years > 3);

    -- Query 2: Nested subquery in WHERE clause
    SELECT Name FROM Professors 
    WHERE Faculty_ID IN (SELECT Faculty_ID FROM Faculties WHERE Secretary_ID IN (SELECT Secretary_ID FROM Secretaries));
END
GO

ALTER PROCEDURE ExistsQueries AS
BEGIN
    -- Query 1: Using EXISTS
    SELECT Name FROM Students
    WHERE EXISTS (SELECT 1 FROM Grades WHERE Grades.Student_ID = Students.Student_ID AND Grades.Grade < 5);

    -- Query 2: Nested EXISTS
    SELECT Name FROM Professors
    WHERE EXISTS (SELECT 1 FROM Courses WHERE Courses.Faculty_ID = Professors.Faculty_ID AND EXISTS (SELECT 1 FROM Classes  WHERE Classes.Course_ID = Courses.Course_ID));
END
GO

ALTER PROCEDURE SubqueryInFrom AS
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




ALTER PROCEDURE GroupByQueries AS
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

ALTER PROCEDURE FinalQueries AS
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


ALTER PROCEDURE AnyAllQueries AS
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
