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
CREATE DATABASE IF NOT EXISTS vacation_destinations_ang;
USE vacation_destinations_ang;

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
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
EOF

if [ $? -ne 0 ]; then
    echo "Error creating database or tables. Please check your MySQL installation."
    exit 1
fi
