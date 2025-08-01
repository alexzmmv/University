<?php

require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/Country.php';

class Destination {
    public $id;
    public $name;
    public $country_id;
    public $description;
    public $tourist_targets;
    public $cost_per_day;
    public $created_at;
    
  
    public static function getAll($page = 1, $itemsPerPage = 10, $filters = []) {
        $conn = getDbConnection();
        $offset = ($page - 1) * $itemsPerPage;
        
        $whereConditions = [];
        $params = [];
        
        if (!empty($filters['countries']) && is_array($filters['countries'])) {
            $countryPlaceholders = [];
            foreach ($filters['countries'] as $index => $countryId) {
                $paramName = ":country_id_" . $index;
                $countryPlaceholders[] = $paramName;
                $params[$paramName] = (int)$countryId;
            }
            
            if (!empty($countryPlaceholders)) {
                $whereConditions[] = "d.country_id IN (" . implode(", ", $countryPlaceholders) . ")";
            }
        }
        
        if (isset($filters['min_cost']) && is_numeric($filters['min_cost'])) {
            $whereConditions[] = "d.cost_per_day >= :min_cost";
            $params[':min_cost'] = (float)$filters['min_cost'];
        }
        
        if (isset($filters['max_cost']) && is_numeric($filters['max_cost'])) {
            $whereConditions[] = "d.cost_per_day <= :max_cost";
            $params[':max_cost'] = (float)$filters['max_cost'];
        }
        
        if (!empty($filters['search'])) {
            $whereConditions[] = "(d.name LIKE :search OR d.description LIKE :search OR c.name LIKE :search)";
            $params[':search'] = "%" . $filters['search'] . "%";
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
    
    public static function getById($id) {
        $conn = getDbConnection();
        $stmt = $conn->prepare("SELECT d.*, c.name as country_name 
                               FROM destinations d 
                               JOIN countries c ON d.country_id = c.id 
                               WHERE d.id = :id");
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetch();
    }
    
    public static function create($data) {
        if (empty($data['name']) || empty($data['country']) || !isset($data['cost_per_day'])) {
            throw new Exception("Name, country, and cost per day are required fields.");
        }
        
        if (!is_numeric($data['cost_per_day']) || $data['cost_per_day'] <= 0) {
            throw new Exception("Cost per day must be a positive number.");
        }
        
        $conn = getDbConnection();
        
        $countryId = Country::addOrGet($data['country']);
        
        $stmt = $conn->prepare("INSERT INTO destinations (name, country_id, description, tourist_targets, cost_per_day) 
                              VALUES (:name, :country_id, :description, :tourist_targets, :cost_per_day)");
        
        $stmt->bindParam(':name', $data['name'], PDO::PARAM_STR);
        $stmt->bindParam(':country_id', $countryId, PDO::PARAM_INT);
        $stmt->bindParam(':description', $data['description'], PDO::PARAM_STR);
        $stmt->bindParam(':tourist_targets', $data['tourist_targets'], PDO::PARAM_STR);
        $stmt->bindParam(':cost_per_day', $data['cost_per_day'], PDO::PARAM_STR);
        
        $stmt->execute();
        return $conn->lastInsertId();
    }
    
    public static function update($id, $data) {
        if (empty($data['name']) || empty($data['country']) || !isset($data['cost_per_day'])) {
            throw new Exception("Name, country, and cost per day are required fields.");
        }
        
        if (!is_numeric($data['cost_per_day']) || $data['cost_per_day'] <= 0) {
            throw new Exception("Cost per day must be a positive number.");
        }
        
        $conn = getDbConnection();
        
        $countryId = Country::addOrGet($data['country']);
        
        $stmt = $conn->prepare("UPDATE destinations 
                              SET name = :name, country_id = :country_id, description = :description, 
                              tourist_targets = :tourist_targets, cost_per_day = :cost_per_day 
                              WHERE id = :id");
        
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        $stmt->bindParam(':name', $data['name'], PDO::PARAM_STR);
        $stmt->bindParam(':country_id', $countryId, PDO::PARAM_INT);
        $stmt->bindParam(':description', $data['description'], PDO::PARAM_STR);
        $stmt->bindParam(':tourist_targets', $data['tourist_targets'], PDO::PARAM_STR);
        $stmt->bindParam(':cost_per_day', $data['cost_per_day'], PDO::PARAM_STR);
        
        return $stmt->execute();
    }
    
    public static function delete($id) {
        $conn = getDbConnection();
        $stmt = $conn->prepare("DELETE FROM destinations WHERE id = :id");
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        return $stmt->execute();
    }
    
    public static function getCostRange() {
        $conn = getDbConnection();
        
        $query = "SELECT MIN(cost_per_day) as min_cost, MAX(cost_per_day) as max_cost FROM destinations";
        $stmt = $conn->prepare($query);
        $stmt->execute();
        
        $result = $stmt->fetch();
        
        return [
            'min_cost' => $result ? (float)$result['min_cost'] : 0,
            'max_cost' => $result ? (float)$result['max_cost'] : 10000000
        ];
    }
}
?>