<?php

require_once '../includes/destination_functions.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $deleted = deleteDestination($id);
        if ($deleted) {
            header('Location: ../index.php?success=' . urlencode('Destination deleted successfully'));
            exit;
        } else {
            $error = 'Failed to delete destination.';
        }
    } catch (Exception $e) {
        $error = 'Error deleting destination: ' . $e->getMessage();
    }
} else {
    $destination = getDestinationById($id);
    
    if (!$destination) {
        header('Location: ../index.php?error=' . urlencode('Destination not found'));
        exit;
    }
}

include '../includes/header.php';
?>

<h2>Delete Destination</h2>

<?php if (isset($error)): ?>
    <div class="alert alert-danger"><?php echo htmlspecialchars($error); ?></div>
<?php endif; ?>

<div class="confirmation">
    <h3>Are you sure you want to delete this destination?</h3>
    
    <div class="destination-summary">
        <p><strong>Name:</strong> <?php echo htmlspecialchars($destination['name']); ?></p>
        <p><strong>Country:</strong> <?php echo htmlspecialchars($destination['country_name']); ?></p>
    </div>
    
    <form method="POST">
        <button type="submit" class="btn btn-danger">Yes, Delete</button>
        <a href="../index.php" class="btn">Cancel</a>
    </form>
</div>

<?php include '../includes/footer.php'; ?>