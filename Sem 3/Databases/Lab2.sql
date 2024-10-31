
USE University;

INSERT INTO Buildings (Name, Address) VALUES ('Main Building', '123 University Ave');

INSERT INTO Rooms (Building_ID, Name, Capacity, Floor, Equipment, AV_Facilities) 
VALUES (1, '101', 50, 1, 'Projector, Chairs', 'Sound System');

INSERT INTO Secretaries( Name,Email,Phone,Office_Location)
VALUES('Pop Alina','popalina@uni.ro','+4075249256','Cluj-napoca Str. Cantemir Nr. 23 Ap 24');

INSERT INTO Faculties (Name, Secretary_ID, Dean, Established) 
VALUES ('Faculty of Science', 1, 'Dr. John Doe', '2000-09-01');

INSERT INTO Students (Name, Date_of_Birth, Profile_ID, Email, Phone, Enrollment_Date) 
VALUES ('Alice Smith', '2001-04-23', 99, 'alice.smith@example.com', '123456789', '2023-09-01');

