<?php
class User {
    private $conn;
    private $table_name = "User";

    public $id;
    public $name;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function getid($name) {
        $query = "SELECT id FROM " . $this->table_name . " WHERE name = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $name);
        $stmt->execute();
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        return $result ? $result['id'] : null;
    }
}
?>
