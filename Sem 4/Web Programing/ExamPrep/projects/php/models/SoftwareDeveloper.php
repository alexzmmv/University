<?php
class SoftwareDeveloper {
    private $conn;
    private $table_name = "SoftwareDeveloper";

    public $id;
    public $name;
    public $age;
    public $skills;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Get all developers
    public function readAll() {
        $query = "SELECT * FROM " . $this->table_name . " ORDER BY name";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }

    // Get developer by name
    public function readByName($name) {
        $query = "SELECT * FROM " . $this->table_name . " WHERE name = ? LIMIT 1";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $name);
        $stmt->execute();
        return $stmt;
    }

    // Get developer by ID
    public function readById($id) {
        $query = "SELECT * FROM " . $this->table_name . " WHERE id = ? LIMIT 1";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $id);
        $stmt->execute();
        return $stmt;
    }

    // Check if developer exists by name
    public function exists($name) {
        $query = "SELECT COUNT(*) as count FROM " . $this->table_name . " WHERE name = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $name);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        return $row['count'] > 0;
    }

    // Create new developer
    public function create() {
        $query = "INSERT INTO " . $this->table_name . " SET name=:name, age=:age, skills=:skills";
        $stmt = $this->conn->prepare($query);

        $this->name = htmlspecialchars(strip_tags($this->name));
        $this->age = htmlspecialchars(strip_tags($this->age));
        $this->skills = htmlspecialchars(strip_tags($this->skills));

        $stmt->bindParam(":name", $this->name);
        $stmt->bindParam(":age", $this->age);
        $stmt->bindParam(":skills", $this->skills);

        if($stmt->execute()) {
            return true;
        }
        return false;
    }
}
?>
