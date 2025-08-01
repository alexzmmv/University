<?php

require_once __DIR__ . '/../config/database.php';

class Country {
    public $id;
    public $name;
    

    public static function getAll() {
        $conn = getDbConnection();
        $stmt = $conn->prepare("SELECT * FROM countries ORDER BY name ASC");
        $stmt->execute();
        return $stmt->fetchAll();
    }
    
    public static function getById($id) {
        $conn = getDbConnection();
        $stmt = $conn->prepare("SELECT * FROM countries WHERE id = :id");
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetch();
    }
    
    public static function addOrGet($name) {
        $conn = getDbConnection();
        
        $stmt = $conn->prepare("SELECT id FROM countries WHERE name = :name");
        $stmt->bindParam(':name', $name, PDO::PARAM_STR);
        $stmt->execute();
        
        if ($stmt->rowCount() > 0) {
            $row = $stmt->fetch();
            return $row['id'];
        }
        
        $stmt = $conn->prepare("INSERT INTO countries (name) VALUES (:name)");
        $stmt->bindParam(':name', $name, PDO::PARAM_STR);
        $stmt->execute();
        
        return $conn->lastInsertId();
    }
    
    public static function getWithDestinations() {
        $conn = getDbConnection();
        $stmt = $conn->prepare("
            SELECT DISTINCT c.* 
            FROM countries c
            INNER JOIN destinations d ON c.id = d.country_id
            ORDER BY c.name ASC
        ");
        $stmt->execute();
        return $stmt->fetchAll();
    }
}
?>