GO
CREATE DATABASE University;
GO
USE University;
GO

-- Create Buildings table
CREATE TABLE Buildings (
    Building_ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(200) NOT NULL
);

-- Create Rooms table
CREATE TABLE Rooms (
    Room_ID INT PRIMARY KEY IDENTITY(1,1),
    Building_ID INT REFERENCES Buildings(Building_ID),
    Room_Number VARCHAR(10) NOT NULL,
    Capacity INT NOT NULL,
    Equipment VARCHAR(255),
    AV_Facilities VARCHAR(255)
);

-- Create Secretaries table
CREATE TABLE Secretaries (
    Secretary_ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Office_Location VARCHAR(100) NOT NULL
);

-- Create Faculties table
CREATE TABLE Faculties (
    Faculty_ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Secretary_ID INT REFERENCES Secretaries(Secretary_ID),
    Dean VARCHAR(100) NOT NULL,
    Established DATE NOT NULL
);

-- Create Profiles table
CREATE TABLE Profiles (
    Profile_ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    Faculty_ID INT REFERENCES Faculties(Faculty_ID),
    Duration_Years INT NOT NULL,
    Degree_Type VARCHAR(50) NOT NULL
);

-- Create Students table
CREATE TABLE Students (
    Student_ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(100) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Email VARCHAR(100) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    EnrollmentDate DATE NOT NULL,
    Profile_ID INT REFERENCES Profiles(Profile_ID)
);

-- Create Courses table
CREATE TABLE Courses (
    Course_ID INT PRIMARY KEY IDENTITY(1,1),
    Code VARCHAR(10) NOT NULL UNIQUE,
    Name VARCHAR(100) NOT NULL,
    Semester INT NOT NULL,
    Credit_Hours INT NOT NULL,
    Description VARCHAR(MAX),
    Faculty_ID INT REFERENCES Faculties(Faculty_ID)
);

-- Create Student_Courses table
CREATE TABLE Student_Courses (
    Student_Course_ID INT PRIMARY KEY IDENTITY(1,1),
    Student_ID INT REFERENCES Students(Student_ID),
    Course_ID INT REFERENCES Courses(Course_ID),
    EnrollmentDate DATE NOT NULL DEFAULT GETDATE()
);

-- Create LogTable for tracking operations
CREATE TABLE LogTable (
    Log_ID INT IDENTITY(1,1) PRIMARY KEY,
    TypeOperation VARCHAR(50) NOT NULL,
    TableOperation VARCHAR(50) NOT NULL,
    ExecutionDate DATETIME DEFAULT GETDATE(),
    ExtraInfo VARCHAR(500) NULL
);
GO
