<?php

require_once '../includes/destination_functions.php';

header('Content-Type: application/json');

$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$countryId = isset($_GET['country_id']) && !empty($_GET['country_id']) ? (int)$_GET['country_id'] : null;

$result = getDestinationsWithPagination($page, 4, $countryId);

echo json_encode($result);
exit;