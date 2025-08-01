<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

require_once '../config/database.php';
require_once '../models/Product.php';

$database = new Database();
$db = $database->getConnection();

$product = new Product($db);

$method = $_SERVER['REQUEST_METHOD'];

if($method == 'GET') {
    $stmt = $product->readAll();
    $products = array();

    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        // Extract category from name using the same logic as in Product model
        $categoryData = $product->extractCategoryFromName($row['name']);
        
        $products[] = array(
            "id" => $row['id'],
            "name" => $categoryData['name'],
            "price" => $row['price'],
            "category" => $categoryData['category']
        );
    }

    http_response_code(200);
    echo json_encode($products);
} else {
    http_response_code(405);
    echo json_encode(array("message" => "Method not allowed"));
}
?>
            