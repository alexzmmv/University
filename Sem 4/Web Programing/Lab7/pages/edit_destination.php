<?php

require_once '../includes/destination_functions.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;

$error = '';
$success = '';

$destination = getDestinationById($id);

if (!$destination) {
    header('Location: ../index.php?error=' . urlencode('Destination not found'));
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $country = trim($_POST['country'] ?? '');
    $description = trim($_POST['description'] ?? '');
    $tourist_targets = trim($_POST['tourist_targets'] ?? '');
    $cost_per_day = trim($_POST['cost_per_day'] ?? '');
    $security_level = trim($_POST['security_level'] ?? '');
    
    if (empty($name) || empty($country) || empty($cost_per_day) || empty($security_level)) {
        $error = 'Name, country, cost per day, and security level are required fields.';
    } elseif (!is_numeric($cost_per_day) || $cost_per_day <= 0) {
        $error = 'Cost per day must be a positive number.';
    } elseif (!in_array($security_level, ['1', '2', '3'])) {
        $error = 'Invalid security level selected.';
    } else {
        $data = [
            'name' => $name,
            'country' => $country,
            'description' => $description,
            'tourist_targets' => $tourist_targets,
            'cost_per_day' => $cost_per_day,
            'security_level' => $security_level
        ];
        
        try {
            updateDestination($id, $data);
            $success = 'Destination updated successfully!';
            
            $destination = getDestinationById($id);
        } catch (Exception $e) {
            $error = 'Error updating destination: ' . $e->getMessage();
        }
    }
}

include '../includes/header.php';
?>

<h2>Edit Destination</h2>

<?php if ($error): ?>
    <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
<?php endif; ?>

<?php if ($success): ?>
    <div class="alert alert-success"><?php echo htmlspecialchars($success); ?></div>
<?php endif; ?>

<form method="POST" id="destination-form">
    <div class="form-group">
        <label for="name">Destination Name *</label>
        <input type="text" id="name" name="name" value="<?php echo htmlspecialchars($destination['name']); ?>" required>
    </div>
    
    <div class="form-group">
        <label for="country">Country *</label>
        <input type="text" id="country" name="country" value="<?php echo htmlspecialchars($destination['country_name']); ?>" required>
    </div>
    
    <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" name="description" rows="4"><?php echo htmlspecialchars($destination['description']); ?></textarea>
    </div>
    
    <div class="form-group">
        <label for="tourist_targets">Tourist Targets</label>
        <textarea id="tourist_targets" name="tourist_targets" rows="4"><?php echo htmlspecialchars($destination['tourist_targets']); ?></textarea>
    </div>
    
    <div class="form-group">
        <label for="cost_per_day">Cost Per Day ($) *</label>
        <input type="number" id="cost_per_day" name="cost_per_day" value="<?php echo htmlspecialchars($destination['cost_per_day']); ?>" step="0.01" min="0" required>
    </div>
    
    <div class="form-group">
        <label for="security_level">Security Level *</label>
        <select id="security_level" name="security_level" required>
            <option value="1" <?php echo isset($destination['security_level']) && $destination['security_level'] == 1 ? 'selected' : ''; ?>>High Security</option>
            <option value="2" <?php echo isset($destination['security_level']) && $destination['security_level'] == 2 ? 'selected' : ''; ?>>Medium Security</option>
            <option value="3" <?php echo isset($destination['security_level']) && $destination['security_level'] == 3 ? 'selected' : ''; ?>>Low Security</option>
        </select>
        <small class="form-text">High = Extremely safe, Medium = Take normal precautions, Low = Exercise increased caution</small>
    </div>
    
    <button type="submit" class="btn" onclick="">Update Destination</button>
    <a href="../index.php" class="btn btn-secondary" onclick="return confirm('Are you sure you want to cancel? Any unsaved changes will be lost.');">Cancel</a>
</form>

<?php include '../includes/footer.php'; ?>