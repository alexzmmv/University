package com.projectmanagement.config;

import javax.sql.DataSource;
import org.apache.commons.dbcp2.BasicDataSource;
import java.sql.Connection;
import java.sql.SQLException;

public class DatabaseConfig {
    private static final String DB_URL = "jdbc:mysql://localhost:3306/project_management?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true&useUnicode=true&characterEncoding=UTF-8";
    private static final String DB_USERNAME = "root";
    private static final String DB_PASSWORD = "";
    private static final String DB_DRIVER = "com.mysql.cj.jdbc.Driver";
    
    private static DataSource dataSource;
    
    static {
        try {
            // Load the MySQL driver explicitly
            Class.forName(DB_DRIVER);
            
            BasicDataSource ds = new BasicDataSource();
            ds.setDriverClassName(DB_DRIVER);
            ds.setUrl(DB_URL);
            ds.setUsername(DB_USERNAME);
            ds.setPassword(DB_PASSWORD);
            
            // Connection pool settings
            ds.setMinIdle(2);
            ds.setMaxIdle(10);
            ds.setMaxTotal(50);
            ds.setMaxOpenPreparedStatements(100);
            
            // Connection validation
            ds.setTestOnBorrow(true);
            ds.setValidationQuery("SELECT 1");
            ds.setTestWhileIdle(true);
            ds.setTimeBetweenEvictionRunsMillis(60000);
            
            // Connection timeout settings
            ds.setMaxWaitMillis(10000);
            
            dataSource = ds;
            
            // Test the connection
            try (Connection testConn = ds.getConnection()) {
                System.out.println("✅ Database connection established successfully!");
            }
            
        } catch (ClassNotFoundException e) {
            System.err.println("❌ MySQL Driver not found: " + e.getMessage());
            throw new RuntimeException("MySQL Driver not found", e);
        } catch (SQLException e) {
            System.err.println("❌ Database connection failed: " + e.getMessage());
            System.err.println("Please check:");
            System.err.println("1. MySQL server is running");
            System.err.println("2. Database 'project_management' exists");
            System.err.println("3. Username/password are correct");
            throw new RuntimeException("Database connection failed", e);
        }
    }
    
    public static Connection getConnection() throws SQLException {
        try {
            return dataSource.getConnection();
        } catch (SQLException e) {
            System.err.println("❌ Failed to get database connection: " + e.getMessage());
            throw e;
        }
    }
    
    public static DataSource getDataSource() {
        return dataSource;
    }
}
