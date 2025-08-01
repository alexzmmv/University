<?php
class Project {
    private $conn;
    private $table_name = "Project";

    public $id;
    public $ProjectManagerID;
    public $name;
    public $description;
    public $members;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Get all projects
    public function readAll() {
        $query = "SELECT p.*, s.name as manager_name 
                  FROM " . $this->table_name . " p 
                  LEFT JOIN SoftwareDeveloper s ON p.ProjectManagerID = s.id 
                  ORDER BY p.name";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }

    // Get projects where user is a member
    public function readByMember($memberName) {
        $query = "SELECT * FROM " . $this->table_name . " WHERE members LIKE ? ORDER BY name";
        $stmt = $this->conn->prepare($query);
        $searchTerm = "%" . $memberName . "%";
        $stmt->bindParam(1, $searchTerm);
        $stmt->execute();
        return $stmt;
    }

    // Check if project exists by name
    public function exists($name) {
        $query = "SELECT COUNT(*) as count FROM " . $this->table_name . " WHERE name = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $name);
        $stmt->execute();
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        return $row['count'] > 0;
    }

    // Create new project
    public function create() {
        $query = "INSERT INTO " . $this->table_name . " SET name=:name, description=:description, members=:members, ProjectManagerID=:ProjectManagerID";
        $stmt = $this->conn->prepare($query);

        $this->name = htmlspecialchars(strip_tags($this->name));
        $this->description = htmlspecialchars(strip_tags($this->description));
        $this->members = htmlspecialchars(strip_tags($this->members));

        $stmt->bindParam(":name", $this->name);
        $stmt->bindParam(":description", $this->description);
        $stmt->bindParam(":members", $this->members);
        $stmt->bindParam(":ProjectManagerID", $this->ProjectManagerID);

        if($stmt->execute()) {
            return true;
        }
        return false;
    }

    // Update project members
    public function updateMembers($projectName, $newMember) {
        // Get current project
        $query = "SELECT * FROM " . $this->table_name . " WHERE name = ?";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $projectName);
        $stmt->execute();
        $project = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($project) {
            $currentMembers = $project['members'];
            
            // Check if member is already in the list
            if (strpos($currentMembers, $newMember) === false) {
                $updatedMembers = $currentMembers ? $currentMembers . ", " . $newMember : $newMember;
                
                // Update the project
                $updateQuery = "UPDATE " . $this->table_name . " SET members = ? WHERE name = ?";
                $updateStmt = $this->conn->prepare($updateQuery);
                $updateStmt->bindParam(1, $updatedMembers);
                $updateStmt->bindParam(2, $projectName);
                return $updateStmt->execute();
            }
        }
        return false;
    }
}
?>
