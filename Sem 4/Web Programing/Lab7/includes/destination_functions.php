<?php

require_once 'db_config.php';

function getAllCountries() {
    $conn = getDbConnection();
    $stmt = $conn->prepare("SELECT * FROM countries ORDER BY name ASC");
    $stmt->execute();
    return $stmt->fetchAll();
}

function getCountryById($id) {
    $conn = getDbConnection();
    $stmt = $conn->prepare("SELECT * FROM countries WHERE id = :id");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetch();
}


function addCountry($name) {
    $conn = getDbConnection();
    
    $stmt = $conn->prepare("SELECT id FROM countries WHERE name = :name");
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->execute();
    
    if ($stmt->rowCount() > 0) {
        $row = $stmt->fetch();
        return $row['id'];
    }
    
    $stmt = $conn->prepare("INSERT INTO countries (name) VALUES (:name)");
    $stmt->bindParam(':name', $name, PDO::PARAM_STR);
    $stmt->execute();
    
    return $conn->lastInsertId();
}

function getDestinationsWithAdvancedFilters($page = 1, $itemsPerPage = 4, $filters = []) {
    $conn = getDbConnection();
    $offset = ($page - 1) * $itemsPerPage;
    
    $whereConditions = [];
    $params = [];
    
    if (!empty($filters['countries']) && is_array($filters['countries'])) {
        $countryPlaceholders = [];
        foreach ($filters['countries'] as $index => $countryId) {
            $countryId = filter_var($countryId, FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
            if ($countryId !== false) {
                $paramName = ":country_id_" . $index;
                $countryPlaceholders[] = $paramName;
                $params[$paramName] = $countryId;
            }
        }
        
        if (!empty($countryPlaceholders)) {
            $whereConditions[] = "d.country_id IN (" . implode(", ", $countryPlaceholders) . ")";
        }
    }
    
    if (isset($filters['security_level'])) {
        $securityLevel = filter_var($filters['security_level'], FILTER_VALIDATE_INT);
        if ($securityLevel !== false && $securityLevel >= 1 && $securityLevel <= 3) {
            $whereConditions[] = "d.security_level = :security_level";
            $params[':security_level'] = $securityLevel;
        }
    }
    
    if (isset($filters['min_cost'])) {
        $minCost = filter_var($filters['min_cost'], FILTER_VALIDATE_FLOAT);
        if ($minCost !== false) {
            $whereConditions[] = "d.cost_per_day >= :min_cost";
            $params[':min_cost'] = $minCost;
        }
    }
    
    if (isset($filters['max_cost'])) {
        $maxCost = filter_var($filters['max_cost'], FILTER_VALIDATE_FLOAT);
        if ($maxCost !== false) {
            $whereConditions[] = "d.cost_per_day <= :max_cost";
            $params[':max_cost'] = $maxCost;
        }
    }
    
    if (!empty($filters['search'])) {
        $searchTerm = htmlspecialchars(trim($filters['search']), ENT_QUOTES, 'UTF-8');
        if (!empty($searchTerm)) {
            $whereConditions[] = "(d.name LIKE :search OR d.description LIKE :search OR c.name LIKE :search)";
            $params[':search'] = "%" . $searchTerm . "%";
        }
    }
    
    $whereClause = !empty($whereConditions) ? "WHERE " . implode(" AND ", $whereConditions) : "";
    
    $countQuery = "SELECT COUNT(*) as total FROM destinations d 
                  JOIN countries c ON d.country_id = c.id 
                  $whereClause";
    
    $countStmt = $conn->prepare($countQuery);
    foreach ($params as $param => $value) {
        $countStmt->bindValue($param, $value);
    }
    $countStmt->execute();
    $totalItems = $countStmt->fetch()['total'];
    
    $totalPages = ceil($totalItems / $itemsPerPage);
    
    $currentPage = max(1, min($page, $totalPages > 0 ? $totalPages : 1));
    
    $query = "SELECT d.*, c.name as country_name 
              FROM destinations d 
              JOIN countries c ON d.country_id = c.id 
              $whereClause
              ORDER BY d.name ASC 
              LIMIT :offset, :limit";
    
    $stmt = $conn->prepare($query);
    foreach ($params as $param => $value) {
        $stmt->bindValue($param, $value);
    }
    $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
    $stmt->bindValue(':limit', $itemsPerPage, PDO::PARAM_INT);
    
    $stmt->execute();
    $destinations = $stmt->fetchAll();
    
    return [
        'destinations' => $destinations,
        'pagination' => [
            'currentPage' => $currentPage,
            'totalPages' => $totalPages,
            'totalItems' => $totalItems,
            'itemsPerPage' => $itemsPerPage
        ],
        'filters' => $filters
    ];
}

function getCostRange() {
    $conn = getDbConnection();
    
    $query = "SELECT MIN(cost_per_day) as min_cost, MAX(cost_per_day) as max_cost FROM destinations";
    $stmt = $conn->prepare($query);
    $stmt->execute();
    
    $result = $stmt->fetch();
    
    // Provide defaults if no data exists
    return [
        'min_cost' => $result ? (float)$result['min_cost'] : 0,
        'max_cost' => $result ? (float)$result['max_cost'] : 1000
    ];
}


function getDestinationsWithPagination($page = 1, $itemsPerPage = 4, $countryId = null) {
    $filters = [];
    
    if ($countryId !== null) {
        $filters['countries'] = [(int)$countryId];
    }
    
    return getDestinationsWithAdvancedFilters($page, $itemsPerPage, $filters);
}


function getDestinationById($id) {
    $conn = getDbConnection();
    $stmt = $conn->prepare("SELECT d.*, c.name as country_name 
                           FROM destinations d 
                           JOIN countries c ON d.country_id = c.id 
                           WHERE d.id = :id");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    return $stmt->fetch();
}

function addDestination($data) {
    $conn = getDbConnection();
    
    // Make sure country exists or create it
    $countryId = addCountry($data['country']);
    
    $stmt = $conn->prepare("INSERT INTO destinations (name, country_id, description, tourist_targets, cost_per_day, security_level) 
                          VALUES (:name, :country_id, :description, :tourist_targets, :cost_per_day, :security_level)");
    
    $stmt->bindParam(':name', $data['name'], PDO::PARAM_STR);
    $stmt->bindParam(':country_id', $countryId, PDO::PARAM_INT);
    $stmt->bindParam(':description', $data['description'], PDO::PARAM_STR);
    $stmt->bindParam(':tourist_targets', $data['tourist_targets'], PDO::PARAM_STR);
    $stmt->bindParam(':cost_per_day', $data['cost_per_day'], PDO::PARAM_STR);
    $stmt->bindParam(':security_level', $data['security_level'], PDO::PARAM_INT);
    
    $stmt->execute();
    return $conn->lastInsertId();
}

function updateDestination($id, $data) {
    $conn = getDbConnection();
    
    $countryId = addCountry($data['country']);
    
    $stmt = $conn->prepare("UPDATE destinations 
                          SET name = :name, country_id = :country_id, description = :description, 
                          tourist_targets = :tourist_targets, cost_per_day = :cost_per_day, security_level = :security_level
                          WHERE id = :id");
    
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->bindParam(':name', $data['name'], PDO::PARAM_STR);
    $stmt->bindParam(':country_id', $countryId, PDO::PARAM_INT);
    $stmt->bindParam(':description', $data['description'], PDO::PARAM_STR);
    $stmt->bindParam(':tourist_targets', $data['tourist_targets'], PDO::PARAM_STR);
    $stmt->bindParam(':cost_per_day', $data['cost_per_day'], PDO::PARAM_STR);
    $stmt->bindParam(':security_level', $data['security_level'], PDO::PARAM_INT);
    
    return $stmt->execute();
}

function deleteDestination($id) {
    $conn = getDbConnection();
    $stmt = $conn->prepare("DELETE FROM destinations WHERE id = :id");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    return $stmt->execute();
}

function getSecurityLevels($includeAny = false) {
    $levels = [];
    
    if ($includeAny) {
        $levels[] = [
            'id' => 0,
            'name' => 'Any Security Level'
        ];
    }
    
    for ($i = 1; $i <= 3; $i++) {
        $securityName = "";
        switch($i) {
            case 1:
                $securityName = "High Security";
                break;
            case 2:
                $securityName = "Medium Security";
                break;
            case 3:
                $securityName = "Low Security";
                break;
        }
        $levels[] = [
            'id' => $i,
            'name' => $securityName
        ];
    }
    return $levels;
}

function getCountriesWithDestinations() {
    $conn = getDbConnection();
    $stmt = $conn->prepare("
        SELECT DISTINCT c.* 
        FROM countries c
        INNER JOIN destinations d ON c.id = d.country_id
        ORDER BY c.name ASC
    ");
    $stmt->execute();
    return $stmt->fetchAll();
}
?>