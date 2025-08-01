<?php

require_once __DIR__ . '/../../config/api_utils.php';
require_once __DIR__ . '/../../models/Destination.php';

enableCORS();

$method = $_SERVER['REQUEST_METHOD'];

$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$pathSegments = explode('/', trim($requestUri, '/'));
$apiIndex = array_search('api', $pathSegments);
$resourceIndex = $apiIndex + 2; // api/v1/destinations

$id = null;
if (isset($pathSegments[$resourceIndex + 1]) && is_numeric($pathSegments[$resourceIndex + 1])) {
    $id = (int)$pathSegments[$resourceIndex + 1];
}

if (!$id && isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = (int)$_GET['id'];
}

try {
    switch ($method) {
        case 'GET':
            if ($id) {
                $destination = Destination::getById($id);
                if ($destination) {
                    sendJsonResponse($destination);
                } else {
                    sendErrorResponse("Destination not found", 404);
                }
            } elseif (isset($pathSegments[$resourceIndex + 1]) && $pathSegments[$resourceIndex + 1] === 'cost-range') {
                $costRange = Destination::getCostRange();
                sendJsonResponse($costRange);
            } elseif (isset($_GET['action']) && $_GET['action'] === 'cost-range') {
                $costRange = Destination::getCostRange();
                sendJsonResponse($costRange);
            } else {
                $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
                $itemsPerPage = isset($_GET['limit']) ? (int)$_GET['limit'] : 10;
                
                $filters = [];
                
                if (isset($_GET['countries'])) {
                    $countries = explode(',', $_GET['countries']);
                    $filters['countries'] = array_map('intval', $countries);
                }
                
                if (isset($_GET['min_cost'])) {
                    $filters['min_cost'] = (float)$_GET['min_cost'];
                }
                
                if (isset($_GET['max_cost'])) {
                    $filters['max_cost'] = (float)$_GET['max_cost'];
                }
                
                if (isset($_GET['search'])) {
                    $filters['search'] = $_GET['search'];
                }
                
                $result = Destination::getAll($page, $itemsPerPage, $filters);
                sendJsonResponse($result);
            }
            break;
            
        case 'POST':
            validateMethod('POST'); 
            
            $data = getRequestData();
            if (!$data) {
                sendErrorResponse("Invalid JSON data", 400);
            }
            
            $destinationId = Destination::create($data);
            $newDestination = Destination::getById($destinationId);
            
            sendJsonResponse(['message' => 'Destination created successfully', 'destination' => $newDestination], 201);
            break;
            
        case 'PUT':
            if (!$id) {
                sendErrorResponse("Destination ID required for updates", 400);
            }
            
            $destination = Destination::getById($id);
            if (!$destination) {
                sendErrorResponse("Destination not found", 404);
            }
            
            $data = getRequestData();
            if (!$data) {
                sendErrorResponse("Invalid JSON data", 400);
            }
            
            Destination::update($id, $data);
            $updatedDestination = Destination::getById($id);
            
            sendJsonResponse(['message' => 'Destination updated successfully', 'destination' => $updatedDestination]);
            break;
            
        case 'DELETE':
            if (!$id) {
                sendErrorResponse("Destination ID required for deletion", 400);
            }
            
            $destination = Destination::getById($id);
            if (!$destination) {
                sendErrorResponse("Destination not found", 404);
            }
            
            Destination::delete($id);
            
            sendJsonResponse(['message' => 'Destination deleted successfully'], 200);
            break;
            
        default:
            sendErrorResponse("Method not allowed", 405);
            break;
    }
    
} catch (Exception $e) {
    sendErrorResponse($e->getMessage(), 500);
}
?>