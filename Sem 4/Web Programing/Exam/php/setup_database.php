<?php
require_once 'config/database.php';

try {
    $pdo = new PDO("mysql:host=localhost", "root", "");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $pdo->exec("CREATE DATABASE IF NOT EXISTS shop");
    $pdo->exec("USE shop");
    
    $sql_user = "CREATE TABLE IF NOT EXISTS User (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )";
    $pdo->exec($sql_user);
    
    $sql_product = "CREATE TABLE IF NOT EXISTS Product (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10,2)
    )";
    $pdo->exec($sql_product);
    
    $sql_order = "CREATE TABLE IF NOT EXISTS `Order` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        userId int,
        totalPrice DECIMAL(10,2),
        FOREIGN KEY (userId) REFERENCES User(id)
    )";
    $pdo->exec($sql_order);

    $sql_order_item = "CREATE TABLE IF NOT EXISTS OrderItem (
        id INT AUTO_INCREMENT PRIMARY KEY,
        orderId int,
        productId int,
        quantity int DEFAULT 1,
        FOREIGN KEY (orderId) REFERENCES `Order`(id),
        FOREIGN KEY (productId) REFERENCES Product(id)
    )";
    $pdo->exec($sql_order_item);

    $pdo->exec("INSERT IGNORE INTO User (id, name) VALUES 
        (100, 'Alex')");
    
    $pdo->exec("INSERT IGNORE INTO Product (id, name, price) VALUES 
        (1, 'ELECTRONICS-Laptop', 999.99),
        (2, 'ELECTRONICS-Phone', 599.99),
        (3, 'CLOTHING-Shirt', 29.99),
        (4, 'BOOKS-Programming', 49.99),
        (5, 'FOOD-Pizza', 15.99)");

    echo "Database and tables created successfully with sample data!";
    
} catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
}
?> 
 