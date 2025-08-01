<?php
class Product {
    private $conn;
    private $table_name = "Product";

    public $id;
    public $name;
    public $price;
    public $category;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function readAll() {
        $query = "SELECT * FROM " . $this->table_name . "";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }
    
    
    public function getPrice($id) {
        $query = "SELECT price FROM " . $this->table_name . " WHERE id = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $id);
        $stmt->execute();
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        return $result ? $result['price'] : 0;
    }
    
    public function extractCategoryFromName($fullName) {
        if (strpos($fullName, '-') !== false) {
            $parts = explode('-', $fullName, 2);
            return array(
                'category' => $parts[0],
                'name' => $parts[1]
            );
        } else {
            return array(
                'category' => 'GENERAL',
                'name' => $fullName
            );
        }
    }
}
?>
