<?php

require_once __DIR__ . '/../../config/api_utils.php';
require_once __DIR__ . '/../../models/Country.php';

enableCORS();

$method = $_SERVER['REQUEST_METHOD'];

$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$pathSegments = explode('/', trim($requestUri, '/'));
$apiIndex = array_search('api', $pathSegments);
$resourceIndex = $apiIndex + 2;

$id = null;
if (isset($pathSegments[$resourceIndex + 1]) && is_numeric($pathSegments[$resourceIndex + 1])) {
    $id = (int)$pathSegments[$resourceIndex + 1];
}

try {
    switch ($method) {
        case 'GET':
            if ($id) {
                $country = Country::getById($id);
                if ($country) {
                    sendJsonResponse($country);
                } else {
                    sendErrorResponse("Country not found", 404);
                }
            } else {
                $withDestinations = isset($_GET['with_destinations']) && $_GET['with_destinations'] === 'true';
                
                if ($withDestinations) {
                    $countries = Country::getWithDestinations();
                } else {
                    $countries = Country::getAll();
                }
                
                sendJsonResponse(['countries' => $countries]);
            }
            break;
            
        default:
            sendErrorResponse("Method not allowed", 405);
            break;
    }
    
} catch (Exception $e) {
    sendErrorResponse($e->getMessage(), 500);
}
?>