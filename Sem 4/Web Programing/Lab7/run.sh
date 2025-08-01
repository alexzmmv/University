#!/bin/bash

echo "===== Setting up Vacation Destinations Database ====="

# Check if MySQL server is running
echo "Checking MySQL server status..."
if ! pgrep -x "mysqld" > /dev/null; then
    echo "MySQL server is not running. Starting MySQL..."
    
    # For macOS using brew
    if [ -f /usr/local/bin/brew ] || [ -f /opt/homebrew/bin/brew ]; then
        brew services start mysql
    # Direct command
    elif [ -f /usr/local/mysql/bin/mysqld_safe ]; then
        sudo /usr/local/mysql/bin/mysqld_safe &
    else
        echo "Could not find MySQL server. Please start MySQL manually and run this script again."
        exit 1
    fi
    
    echo "Waiting for MySQL to start..."
    sleep 5
else
    echo "MySQL server is already running."
fi

# Create database and tables if they don't exist
echo "Creating database and tables if they don't exist..."
mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS vacation_destinations;
USE vacation_destinations;

CREATE TABLE IF NOT EXISTS countries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS destinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    description TEXT,
    tourist_targets TEXT,
    cost_per_day DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    security_level INT DEFAULT 1 CHECK (security_level BETWEEN 1 AND 3),
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
EOF

if [ $? -ne 0 ]; then
    echo "Error creating database or tables. Please check your MySQL installation."
    exit 1
fi

echo -n "Do you want to insert mock data? (y/n): "
read insert_mock_data

if [[ "$insert_mock_data" =~ ^[Yy]$ ]]; then
    # Run PHP script to insert mock data
    echo "Inserting mock data..."
    php -f "$(dirname "$0")/mock_data.php" > /dev/null

    if [ $? -ne 0 ]; then
        echo "Error executing mock data script."
        exit 1
    fi
    echo "Mock data inserted successfully."
else
    echo "Skipping mock data insertion."
fi

echo "===== Database setup complete! ====="
echo "Database: vacation_destinations"
echo "Username: root"
echo "Password: <none>"
echo ""
