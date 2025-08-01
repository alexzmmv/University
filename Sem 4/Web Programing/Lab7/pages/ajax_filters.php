<?php

require_once '../includes/destination_functions.php';

header('Content-Type: application/json');

$json = file_get_contents('php://input');
$data = json_decode($json, true);

$filters = isset($data['filters']) ? $data['filters'] : [];
$page = isset($data['page']) ? (int)$data['page'] : 1;

$result = getDestinationsWithAdvancedFilters($page, 4, $filters);

echo json_encode($result);
exit;