<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

require_once '../config/database.php';
require_once '../models/Project.php';

$database = new Database();
$db = $database->getConnection();

$project = new Project($db);

$method = $_SERVER['REQUEST_METHOD'];

switch($method) {
    case 'GET':
        // Get all projects
        $stmt = $project->readAll();
        $projects = array();

        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            $projects[] = array(
                "id" => $row['id'],
                "name" => $row['name'],
                "description" => $row['description'],
                "members" => $row['members'],
                "ProjectManagerID" => $row['ProjectManagerID'],
                "manager_name" => $row['manager_name']
            );
        }

        http_response_code(200);
        echo json_encode($projects);
        break;

    case 'POST':
        // Handle different POST actions
        $data = json_decode(file_get_contents("php://input"));
        
        if (isset($data->action)) {
            switch($data->action) {
                case 'get_user_projects':
                    if (!empty($data->username)) {
                        $stmt = $project->readByMember($data->username);
                        $projects = array();

                        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                            $projects[] = array(
                                "id" => $row['id'],
                                "name" => $row['name']
                            );
                        }

                        http_response_code(200);
                        echo json_encode($projects);
                    } else {
                        http_response_code(400);
                        echo json_encode(array("message" => "Username is required."));
                    }
                    break;

                case 'assign_developer':
                    if (!empty($data->developer) && !empty($data->projects)) {
                        require_once '../models/SoftwareDeveloper.php';
                        $developer = new SoftwareDeveloper($db);
                        
                        // Check if developer exists
                        if (!$developer->exists($data->developer)) {
                            http_response_code(400);
                            echo json_encode(array("message" => "Developer does not exist."));
                            break;
                        }

                        $results = array();
                        foreach ($data->projects as $projectName) {
                            // Check if project exists, if not create it
                            if (!$project->exists($projectName)) {
                                $project->name = $projectName;
                                $project->description = "";
                                $project->members = $data->developer;
                                $project->ProjectManagerID = null;
                                
                                if ($project->create()) {
                                    $results[] = array(
                                        "project" => $projectName,
                                        "status" => "created and developer assigned"
                                    );
                                }
                            } else {
                                // Update existing project
                                if ($project->updateMembers($projectName, $data->developer)) {
                                    $results[] = array(
                                        "project" => $projectName,
                                        "status" => "developer assigned"
                                    );
                                } else {
                                    $results[] = array(
                                        "project" => $projectName,
                                        "status" => "developer already assigned or error occurred"
                                    );
                                }
                            }
                        }

                        http_response_code(200);
                        echo json_encode(array("results" => $results));
                    } else {
                        http_response_code(400);
                        echo json_encode(array("message" => "Developer and projects are required."));
                    }
                    break;

                default:
                    http_response_code(400);
                    echo json_encode(array("message" => "Invalid action."));
                    break;
            }
        } else {
            http_response_code(400);
            echo json_encode(array("message" => "Action is required."));
        }
        break;

    default:
        http_response_code(405);
        echo json_encode(array("message" => "Method not allowed."));
        break;
}
?>
