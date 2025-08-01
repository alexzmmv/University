<?php

require_once '../includes/destination_functions.php';

$countries = getCountriesWithDestinations();
$securityLevels = getSecurityLevels(true); // Get security levels with "Any" option
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

if (isset($_GET['security_level']) && intval($_GET['security_level']) > 0) {
    $filters['security_level'] = intval($_GET['security_level']);
}

$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;

$result = getDestinationsWithAdvancedFilters($page, 4, $filters);
$destinations = $result['destinations'];
$pagination = $result['pagination'];

include '../includes/header.php';
?>

<div class="page-layout">
    <div class="side-filters">
        <div class="filter-section advanced-filters">
            <h3>Filter Options</h3>
            
            <form id="filter-form">
                <div class="filter-controls">
                    <div class="filter-group">
                        <label for="search-input">Search</label>
                        <input type="text" id="search-input" placeholder="Search destinations..." value="<?php echo htmlspecialchars($filters['search'] ?? ''); ?>">
                    </div>
                    
                    <div class="filter-group">
                        <label>Price Range ($ per day)</label>
                        <div class="range-slider">
                            <input type="range" id="min-cost" min="<?php echo floor($costRange['min_cost']); ?>" max="<?php echo ceil($costRange['max_cost']); ?>" value="<?php echo isset($filters['min_cost']) ? $filters['min_cost'] : floor($costRange['min_cost']); ?>">
                            <input type="range" id="max-cost" min="<?php echo floor($costRange['min_cost']); ?>" max="<?php echo ceil($costRange['max_cost']); ?>" value="<?php echo isset($filters['max_cost']) ? $filters['max_cost'] : ceil($costRange['max_cost']); ?>">
                            <div class="range-labels">
                                <span id="min-cost-value">$<?php echo isset($filters['min_cost']) ? $filters['min_cost'] : floor($costRange['min_cost']); ?></span>
                                <span id="max-cost-value">$<?php echo isset($filters['max_cost']) ? $filters['max_cost'] : ceil($costRange['max_cost']); ?></span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="filter-group">
                        <label for="security-level">Security Level</label>
                        <select id="security-level" class="form-control">
                            <?php foreach ($securityLevels as $level): ?>
                                <option value="<?php echo $level['id']; ?>" <?php echo (isset($filters['security_level']) && $filters['security_level'] == $level['id']) ? 'selected' : ''; ?>>
                                    <?php echo htmlspecialchars($level['name']); ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>
                
                <div class="filter-group">
                    <label>Select Countries</label>
                    <div class="checkbox-group">
                        <?php foreach ($countries as $country): ?>
                            <div class="checkbox-item">
                                <input type="checkbox" class="country-checkbox" id="country-<?php echo $country['id']; ?>" value="<?php echo $country['id']; ?>" <?php echo (!empty($filters['countries']) && in_array($country['id'], $filters['countries'])) ? 'checked' : ''; ?>>
                                <label for="country-<?php echo $country['id']; ?>"><?php echo htmlspecialchars($country['name']); ?></label>
                            </div>
                        <?php endforeach; ?>
                    </div>
                </div>
                
                <div class="filter-buttons">
                    <button type="button" id="apply-filters" class="btn btn-primary">Apply Filters</button>
                    <button type="button" id="reset-filters" class="btn btn-secondary">Reset Filters</button>
                </div>
            </form>
        </div>
    </div>
    
    <div class="main-content">
        <h2>Browse Destinations</h2>
        
        <div id="destinations-container">
            <?php if (empty($destinations)): ?>
                <p class="no-results">No destinations found matching your criteria.</p>
            <?php else: ?>
                <div class="destinations-grid">
                    <?php foreach ($destinations as $destination): ?>
                        <div class="destination-card" onclick="window.location.href='view_destination.php?id=<?php echo $destination['id']; ?>'">
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

        <div id="pagination-container">
            <?php if ($pagination['totalPages'] > 1): ?>
                <ul class="pagination">
                    <?php if ($pagination['currentPage'] > 1): ?>
                        <li><a href="?page=<?php echo $pagination['currentPage'] - 1; ?><?php echo !empty($filters['countries']) ? '&countries=' . implode(',', $filters['countries']) : ''; ?><?php echo isset($filters['min_cost']) ? '&min_cost=' . $filters['min_cost'] : ''; ?><?php echo isset($filters['max_cost']) ? '&max_cost=' . $filters['max_cost'] : ''; ?><?php echo !empty($filters['search']) ? '&search=' . urlencode($filters['search']) : ''; ?><?php echo isset($filters['security_level']) ? '&security_level=' . $filters['security_level'] : ''; ?>"> Previous</a></li>
                    <?php endif; ?>
                    
                    <?php for ($i = 1; $i <= $pagination['totalPages']; $i++): ?>
                        <li class="<?php echo $i === $pagination['currentPage'] ? 'active' : ''; ?>">
                            <a href="?page=<?php echo $i; ?><?php echo !empty($filters['countries']) ? '&countries=' . implode(',', $filters['countries']) : ''; ?><?php echo isset($filters['min_cost']) ? '&min_cost=' . $filters['min_cost'] : ''; ?><?php echo isset($filters['max_cost']) ? '&max_cost=' . $filters['max_cost'] : ''; ?><?php echo !empty($filters['search']) ? '&search=' . urlencode($filters['search']) : ''; ?><?php echo isset($filters['security_level']) ? '&security_level=' . $filters['security_level'] : ''; ?>"><?php echo $i; ?></a>
                        </li>
                    <?php endfor; ?>
                    
                    <?php if ($pagination['currentPage'] < $pagination['totalPages']): ?>
                        <li><a href="?page=<?php echo $pagination['currentPage'] + 1; ?><?php echo !empty($filters['countries']) ? '&countries=' . implode(',', $filters['countries']) : ''; ?><?php echo isset($filters['min_cost']) ? '&min_cost=' . $filters['min_cost'] : ''; ?><?php echo isset($filters['max_cost']) ? '&max_cost=' . $filters['max_cost'] : ''; ?><?php echo !empty($filters['search']) ? '&search=' . urlencode($filters['search']) : ''; ?><?php echo isset($filters['security_level']) ? '&security_level=' . $filters['security_level'] : ''; ?>">Next </a></li>
                    <?php endif; ?>
                </ul>
            <?php endif; ?>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>