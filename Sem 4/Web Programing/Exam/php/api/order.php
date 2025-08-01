<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

require_once '../config/database.php';
require_once '../models/Order.php';
require_once '../models/OrderItem.php';
require_once '../models/User.php';
require_once '../models/Product.php';

$database = new Database();
$db = $database->getConnection();

$method = $_SERVER['REQUEST_METHOD'];

if($method == 'POST') {
    $data = json_decode(file_get_contents("php://input"));
    
    if(isset($data->userName) && isset($data->items) && is_array($data->items)) {
        $db->beginTransaction();
        
        try {
            $order = new Order($db);
            
            // Search user id
            $user = new User($db);
            $product = new Product($db);
            $userId = $user->getId($data->userName);
            
            if (!$userId) {
                throw new Exception("User not found");
            }
            
            $order->userId = $userId;
                        
            foreach($data->items as $item) {
                $itemPrice = $product->getPrice($item->productId);
                $order->totalPrice += $itemPrice * $item->quantity;
            }
            
            if($order->create()) {
                $totalPrice = 0;
                // Create order items
                foreach($data->items as $item) {
                    $orderItem = new OrderItem($db);
                    $orderItem->orderId = $order->id;
                    $orderItem->productId = $item->productId;
                    $orderItem->quantity = $item->quantity;
                    $totalPrice+= $product->getPrice($item->productId) * $item->quantity;
                    if(!$orderItem->create()) {
                        throw new Exception("Failed to create order item");
                    }
                }
                
                $db->commit();
                
                http_response_code(200);
                echo json_encode(array(
                    "success" => true,
                    "orderId" => $order->id,
                    "price" => $order->totalPrice,
                    "message" => "Order created successfully"
                ));
            } else {
                throw new Exception("Failed to create order: UserId, totalPrice, and items are required");
            }
        } catch(Exception $e) {
            $db->rollback();
            http_response_code(500);
            echo json_encode(array(
                "success" => false,
                "message" => "Failed to create order: " . $e->getMessage()
            ));
        }
    } else {
        http_response_code(400);
        echo json_encode(array(
            "success" => false,
            "message" => "UserId, totalPrice, and items are required"
        ));
    }
} else {
    http_response_code(405);
    echo json_encode(array("message" => "Method not allowed"));
}
?>