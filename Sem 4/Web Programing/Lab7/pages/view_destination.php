<?php
require_once '../includes/destination_functions.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;

$destination = getDestinationById($id);

if (!$destination) {
    header('Location: ../index.php?error=' . urlencode('Destination not found'));
    exit;
}

include '../includes/header.php';
?>

<div class="view-destination">
    <h2><?php echo htmlspecialchars($destination['name']); ?></h2>
    
    <p class="country-name">
        <strong>Country:</strong> <?php echo htmlspecialchars($destination['country_name']); ?>
    </p>
    
    <div class="detail-section">
        <h3>Description</h3>
        <p><?php echo nl2br(htmlspecialchars($destination['description'])); ?></p>
    </div>
    
    <div class="detail-section">
        <h3>Tourist Targets</h3>
        <p><?php echo nl2br(htmlspecialchars($destination['tourist_targets'])); ?></p>
    </div>
    
    <div class="detail-section">
        <h3>Cost Per Day</h3>
        <p class="cost">$<?php echo number_format($destination['cost_per_day'], 2); ?></p>
    </div>
    
    <div class="detail-section">
        <h3> Security Level</h3>
        <?php
        $securityLevel = isset($destination['security_level']) ? (int)$destination['security_level'] : 1;
        $securityText = "";
        $securityClass = "";
        
        switch($securityLevel) {
            case 1:
                $securityText = "High";
                $securityClass = "security-high";
                break;
            case 2:
                $securityText = "Medium";
                $securityClass = "security-medium";
                break;
            case 3:
                $securityText = "Low";
                $securityClass = "security-low";
                break;
            default:
                $securityText = "Unknown";
                $securityClass = "";
        }
        ?>
        <p class="security-detail">
            This destination has <span class="<?php echo $securityClass; ?>"><?php echo $securityText; ?></span> security level.
            <?php if($securityLevel == 1): ?>
                <span class="security-note">Extremely safe for tourists with minimal safety concerns.</span>
            <?php elseif($securityLevel == 2): ?>
                <span class="security-note">Generally safe, but take normal precautions while traveling.</span>
            <?php elseif($securityLevel == 3): ?>
                <span class="security-note">Exercise increased caution and be aware of your surroundings.</span>
            <?php endif; ?>
        </p>
    </div>
    
    <div class="actions">
        <a href="../index.php" class="btn">Back to List</a>
        <a href="edit_destination.php?id=<?php echo $destination['id']; ?>" class="btn btn-secondary">Edit</a>
        <a href="delete_destination.php?id=<?php echo $destination['id']; ?>" class="btn btn-danger delete-btn">Delete</a>
    </div>
</div>

<?php include '../includes/footer.php'; ?>