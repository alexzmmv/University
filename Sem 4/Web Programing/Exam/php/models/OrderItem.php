<?php
class OrderItem {
    private $conn;
    private $table_name = "OrderItem";

    public $id;
    public $orderId;
    public $productId;
    public $quantity;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function create() {
        $query = "INSERT INTO " . $this->table_name . " (orderId, productId, quantity) VALUES (?, ?, ?)";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->orderId);
        $stmt->bindParam(2, $this->productId);
        $stmt->bindParam(3, $this->quantity);
        
        return $stmt->execute();
    }
}
?>
