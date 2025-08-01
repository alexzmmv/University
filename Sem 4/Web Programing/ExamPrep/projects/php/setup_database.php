<?php
require_once 'config/database.php';

try {
    $pdo = new PDO("mysql:host=localhost", "root", "");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $pdo->exec("CREATE DATABASE IF NOT EXISTS project_management");
    $pdo->exec("USE project_management");
    
    $sql_developer = "CREATE TABLE IF NOT EXISTS SoftwareDeveloper (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        skills TEXT
    )";
    $pdo->exec($sql_developer);
    
    $sql_project = "CREATE TABLE IF NOT EXISTS Project (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ProjectManagerID INT,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        members TEXT,
        FOREIGN KEY (ProjectManagerID) REFERENCES SoftwareDeveloper(id)
    )";
    $pdo->exec($sql_project);
    
    $pdo->exec("INSERT IGNORE INTO SoftwareDeveloper (id, name, age, skills) VALUES 
        (1, 'John Doe', 30, 'Java, Python, SQL'),
        (2, 'Jane Smith', 28, 'PHP, JavaScript, HTML'),
        (3, 'Mike Johnson', 35, 'C#, .NET, SQL'),
        (4, 'Sarah Wilson', 26, 'Java, Spring, React'),
        (5, 'David Brown', 32, 'Python, Django, PostgreSQL')");
    
    $pdo->exec("INSERT IGNORE INTO Project (id, ProjectManagerID, name, description, members) VALUES 
        (1, 1, 'E-commerce Platform', 'Online shopping platform', 'John Doe, Jane Smith'),
        (2, 2, 'Mobile App', 'iOS and Android mobile application', 'Jane Smith, Mike Johnson, Sarah Wilson'),
        (3, 3, 'Data Analytics Tool', 'Business intelligence dashboard', 'Mike Johnson, David Brown')");
    
    echo "Database and tables created successfully with sample data!";
    
} catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?>
