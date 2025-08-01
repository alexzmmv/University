<?php

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vacation Destinations Manager</title>
    <link rel="stylesheet" href="<?php echo (strpos($_SERVER['REQUEST_URI'], '/pages/') !== false) ? '../css/styles.css' : 'css/styles.css'; ?>">
</head>
<body>
    <header>
        <div class="container">
            <h1> Vacation Destinations</h1>
            <nav>
                <ul>
                    <li><a href="<?php echo (strpos($_SERVER['REQUEST_URI'], '/pages/') !== false) ? '../index.php' : 'index.php'; ?>"> Home</a></li>
                    <li><a href="<?php echo (strpos($_SERVER['REQUEST_URI'], '/pages/') !== false) ? 'add_destination.php' : 'pages/add_destination.php'; ?>"> Add Destination</a></li>
                    <li><a href="<?php echo (strpos($_SERVER['REQUEST_URI'], '/pages/') !== false) ? 'browse_by_country.php' : 'pages/browse_by_country.php'; ?>"> Browse & Filter</a></li>
                    <li><a href="<?php echo (strpos($_SERVER['REQUEST_URI'], '/pages/') !== false) ? 'about.php' : 'pages/about.php'; ?>"> About</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main class="container">