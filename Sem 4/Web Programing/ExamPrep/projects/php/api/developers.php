<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET, POST");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

require_once '../config/database.php';
require_once '../models/SoftwareDeveloper.php';

$database = new Database();
$db = $database->getConnection();

$developer = new SoftwareDeveloper($db);

$method = $_SERVER['REQUEST_METHOD'];

switch($method) {
    case 'GET':
        // Get all developers
        $stmt = $developer->readAll();
        $developers = array();

        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $developers[] = array(
                "id" => $row['id'],
                "name" => $row['name'],
                "age" => $row['age'],
                "skills" => $row['skills']
            );
        }

        http_response_code(200);
        echo json_encode($developers);
        break;

    case 'POST':
        // Create new developer or other actions
        $data = json_decode(file_get_contents("php://input"));
        
        if (isset($data->action) && $data->action === 'check_user') {
            if (!empty($data->username)) {
                $exists = $developer->exists($data->username);
                http_response_code(200);
                echo json_encode(array("exists" => $exists));
            } else {
                http_response_code(400);
                echo json_encode(array("message" => "Username is required."));
            }
        } else {
            // Create new developer
            if (!empty($data->name)) {
                $developer->name = $data->name;
                $developer->age = isset($data->age) ? $data->age : null;
                $developer->skills = isset($data->skills) ? $data->skills : "";

                if($developer->create()) {
                    http_response_code(201);
                    echo json_encode(array("message" => "Developer created successfully."));
                } else {
                    http_response_code(503);
                    echo json_encode(array("message" => "Unable to create developer."));
                }
            } else {
                http_response_code(400);
                echo json_encode(array("message" => "Name is required."));
            }
        }
        break;

    default:
        http_response_code(405);
        echo json_encode(array("message" => "Method not allowed."));
        break;
}
?>
