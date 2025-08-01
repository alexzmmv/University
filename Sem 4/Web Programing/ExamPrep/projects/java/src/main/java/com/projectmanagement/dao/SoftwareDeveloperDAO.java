package com.projectmanagement.dao;

import com.projectmanagement.config.DatabaseConfig;
import com.projectmanagement.model.SoftwareDeveloper;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class SoftwareDeveloperDAO {
    
    public List<SoftwareDeveloper> getAllDevelopers() throws SQLException {
        List<SoftwareDeveloper> developers = new ArrayList<>();
        String sql = "SELECT * FROM SoftwareDeveloper ORDER BY name";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                SoftwareDeveloper developer = new SoftwareDeveloper(
                    rs.getInt("id"),
                    rs.getString("name"),
                    rs.getObject("age") != null ? rs.getInt("age") : 0,
                    rs.getString("skills") != null ? rs.getString("skills") : ""
                );
                developers.add(developer);
            }
        }
        return developers;
    }
    
    public SoftwareDeveloper getDeveloperByName(String name) throws SQLException {
        String sql = "SELECT * FROM SoftwareDeveloper WHERE name = ? LIMIT 1";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, name);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new SoftwareDeveloper(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getObject("age") != null ? rs.getInt("age") : 0,
                        rs.getString("skills") != null ? rs.getString("skills") : ""
                    );
                }
            }
        }
        return null;
    }
    
    public SoftwareDeveloper getDeveloperById(int id) throws SQLException {
        String sql = "SELECT * FROM SoftwareDeveloper WHERE id = ? LIMIT 1";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setInt(1, id);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return new SoftwareDeveloper(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getObject("age") != null ? rs.getInt("age") : 0,
                        rs.getString("skills") != null ? rs.getString("skills") : ""
                    );
                }
            }
        }
        return null;
    }
    
    public boolean developerExists(String name) throws SQLException {
        String sql = "SELECT COUNT(*) as count FROM SoftwareDeveloper WHERE name = ?";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, name);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("count") > 0;
                }
            }
        }
        return false;
    }
    
    public boolean createDeveloper(SoftwareDeveloper developer) throws SQLException {
        String sql = "INSERT INTO SoftwareDeveloper (name, age, skills) VALUES (?, ?, ?)";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            
            stmt.setString(1, developer.getName());
            stmt.setInt(2, developer.getAge());
            stmt.setString(3, developer.getSkills());
            
            int affectedRows = stmt.executeUpdate();
            
            if (affectedRows > 0) {
                try (ResultSet generatedKeys = stmt.getGeneratedKeys()) {
                    if (generatedKeys.next()) {
                        developer.setId(generatedKeys.getInt(1));
                    }
                }
                return true;
            }
        }
        return false;
    }
}
