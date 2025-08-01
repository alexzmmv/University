<?php
class Order {
    private $conn;
    private $table_name = "`Order`";

    public $id;
    public $userId;
    public $totalPrice;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function create() {
        $query = "INSERT INTO " . $this->table_name . " (userId, totalPrice) VALUES (?, ?)";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->userId);
        $stmt->bindParam(2, $this->totalPrice);
        
        if($stmt->execute()) {
            $this->id = $this->conn->lastInsertId();
            return true;
        }
        return false;
    }
}
?>
