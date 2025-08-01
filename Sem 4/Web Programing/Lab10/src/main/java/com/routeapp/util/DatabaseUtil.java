package com.routeapp.util;

import javax.servlet.ServletContext;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseUtil {
    private static final String DRIVER_CLASS = "com.mysql.cj.jdbc.Driver";
    private static String dbURL;
    private static String dbUser;
    private static String dbPassword;
    private static boolean initialized = false;
    
    static {
        try {
            Class.forName(DRIVER_CLASS);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("MySQL JDBC driver not found", e);
        }
    }
    
    public static void init(ServletContext context) {
        dbURL = context.getInitParameter("dbURL");
        dbUser = context.getInitParameter("dbUser");
        dbPassword = context.getInitParameter("dbPassword");
        
        if (dbURL == null) {
            dbURL = "jdbc:mysql://localhost:3306/routeappdb?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
        }
        if (dbUser == null) {
            dbUser = "root";
        }
        if (dbPassword == null) {
            dbPassword = "";
        }
        
        initializeDatabase();
    }
    
    public static Connection getConnection() throws SQLException {
        if (dbURL == null) {
            dbURL = "jdbc:mysql://localhost:3306/routeappdb?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";
            dbUser = "root";
            dbPassword = ""; 
            initializeDatabase();
        }
        return DriverManager.getConnection(dbURL, dbUser, dbPassword);
    }
    
    private static synchronized void initializeDatabase() {
        if (!initialized) {
            try (Connection conn = DriverManager.getConnection(dbURL, dbUser, dbPassword);
                 java.io.InputStream is = DatabaseUtil.class.getClassLoader().getResourceAsStream("init.sql")) {
                
                if (is != null) {
                    String initScript = new String(is.readAllBytes(), java.nio.charset.StandardCharsets.UTF_8);

                    String[] statements = initScript.split(";");
                    for (String statement : statements) {
                        statement = statement.trim();
                        if (!statement.isEmpty() && !statement.startsWith("--")) {
                            conn.createStatement().execute(statement);
                        }
                    }
                    initialized = true;
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    
    public static void closeConnection(Connection connection) {
        if (connection != null) {
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
