<?php

require_once 'includes/destination_functions.php';

$countries = getCountriesWithDestinations();

$costRange = getCostRange();

$filters = [];

if (isset($_GET['countries'])) {
    $countryIds = explode(',', $_GET['countries']);
    $filters['countries'] = array_map('intval', $countryIds);
}

if (isset($_GET['min_cost'])) {
    $filters['min_cost'] = (float)$_GET['min_cost'];
} else {
    $filters['min_cost'] = $costRange['min_cost'];
}

if (isset($_GET['max_cost'])) {
    $filters['max_cost'] = (float)$_GET['max_cost'];
} else {
    $filters['max_cost'] = $costRange['max_cost'];
}

if (isset($_GET['search'])) {
    $filters['search'] = $_GET['search'];
} else {
    $filters['search'] = '';
}

$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;

$result = getDestinationsWithAdvancedFilters($page, 3, $filters);
$destinations = $result['destinations'];
$pagination = $result['pagination'];

include 'includes/header.php';
?>

<div class="home-banner">
    <h2>Discover Your Next Adventure</h2>
    <p>Explore beautiful destinations from around the world and plan your perfect vacation.</p>
    
    <div class="home-actions">
        <a href="pages/add_destination.php" class="btn btn-primary">Add New Destination</a>
    </div>
</div>

<?php if (isset($_GET['success'])): ?>
    <div class="alert alert-success">
        <?php echo htmlspecialchars($_GET['success']); ?>
    </div>
<?php endif; ?>

<?php if (isset($_GET['error'])): ?>
    <div class="alert alert-danger">
       <?php echo htmlspecialchars($_GET['error']); ?>
    </div>
<?php endif; ?>

<div class="stats-cards">
    <div class="stat-card">
        <h3>Destinations</h3>
        <p class="stat-number"><?php echo $pagination['totalItems']; ?></p>
    </div>
    <div class="stat-card">
        <h3>Countries</h3>
        <p class="stat-number"><?php echo count($countries); ?></p>
    </div>
    <div class="stat-card">
        <h3>Price Range</h3>
        <p class="stat-number">$<?php echo number_format($costRange['min_cost'], 0); ?> - $<?php echo number_format($costRange['max_cost'], 0); ?></p>
    </div>
</div>

<div class="page-layout">
    
    <div class="main-content">
        <h2> Featured Destinations</h2>

        <div id="destinations-container">
            <?php if (empty($destinations)): ?>
                <p class="no-results">No destinations found. <a href="pages/add_destination.php">Add your first destination</a>.</p>
            <?php else: ?>
                <div class="destinations-grid">
                    <?php foreach ($destinations as $destination): ?>
                        <div class="destination-card" onclick="window.location.href='pages/view_destination.php?id=<?php echo $destination['id']; ?>'">
                            <h3><?php echo htmlspecialchars($destination['name']); ?></h3>
                            <div class="country"><?php echo htmlspecialchars($destination['country_name']); ?></div>
                            <p>
                                <?php 
                                $description = htmlspecialchars($destination['description']);
                                echo strlen($description) > 100 ? substr($description, 0, 100) . '...' : $description; 
                                ?>
                            </p>
                            <div class="cost">$<?php echo number_format($destination['cost_per_day'], 2); ?> per day</div>
                            <div class="security-level">
                                Security Level: 
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
                                <span class="<?php echo $securityClass; ?>"><?php echo $securityText; ?></span>
                            </div>
                        </div>
                    <?php endforeach; ?>
                </div>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php include 'includes/footer.php'; ?>