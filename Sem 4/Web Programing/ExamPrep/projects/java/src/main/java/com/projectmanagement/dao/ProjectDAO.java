package com.projectmanagement.dao;

import com.projectmanagement.config.DatabaseConfig;
import com.projectmanagement.model.Project;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProjectDAO {
    
    public List<Project> getAllProjects() throws SQLException {
        List<Project> projects = new ArrayList<>();
        String sql = "SELECT p.*, s.name as manager_name " +
                    "FROM Project p " +
                    "LEFT JOIN SoftwareDeveloper s ON p.ProjectManagerID = s.id " +
                    "ORDER BY p.name";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            
            while (rs.next()) {
                Project project = new Project(
                    rs.getInt("id"),
                    rs.getInt("ProjectManagerID"),
                    rs.getString("name"),
                    rs.getString("description"),
                    rs.getString("members")
                );
                project.setManagerName(rs.getString("manager_name"));
                projects.add(project);
            }
        }
        return projects;
    }
    
    public List<Project> getProjectsByMember(String memberName) throws SQLException {
        List<Project> projects = new ArrayList<>();
        String sql = "SELECT * FROM Project WHERE members LIKE ? ORDER BY name";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            stmt.setString(1, "%" + memberName + "%");
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    Project project = new Project(
                        rs.getInt("id"),
                        rs.getInt("ProjectManagerID"),
                        rs.getString("name"),
                        rs.getString("description"),
                        rs.getString("members")
                    );
                    projects.add(project);
                }
            }
        }
        return projects;
    }
    
    public boolean projectExists(String name) throws SQLException {
        String sql = "SELECT COUNT(*) as count FROM Project WHERE name = ?";
        
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
    
    public boolean createProject(Project project) throws SQLException {
        String sql = "INSERT INTO Project (name, description, members, ProjectManagerID) VALUES (?, ?, ?, ?)";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            
            stmt.setString(1, project.getName());
            stmt.setString(2, project.getDescription());
            stmt.setString(3, project.getMembers());
            if (project.getProjectManagerID() > 0) {
                stmt.setInt(4, project.getProjectManagerID());
            } else {
                stmt.setNull(4, Types.INTEGER);
            }
            
            int affectedRows = stmt.executeUpdate();
            
            if (affectedRows > 0) {
                try (ResultSet generatedKeys = stmt.getGeneratedKeys()) {
                    if (generatedKeys.next()) {
                        project.setId(generatedKeys.getInt(1));
                    }
                }
                return true;
            }
        }
        return false;
    }
    
    public boolean updateProjectMembers(String projectName, String newMember) throws SQLException {
        // First get the current project
        String selectSql = "SELECT * FROM Project WHERE name = ?";
        
        try (Connection conn = DatabaseConfig.getConnection();
             PreparedStatement selectStmt = conn.prepareStatement(selectSql)) {
            
            selectStmt.setString(1, projectName);
            
            try (ResultSet rs = selectStmt.executeQuery()) {
                if (rs.next()) {
                    String currentMembers = rs.getString("members");
                    
                    // Check if member is already in the list
                    if (currentMembers != null && currentMembers.contains(newMember)) {
                        return false; // Member already exists
                    }
                    
                    // Update members
                    String updatedMembers = currentMembers != null && !currentMembers.trim().isEmpty() 
                        ? currentMembers + ", " + newMember 
                        : newMember;
                    
                    String updateSql = "UPDATE Project SET members = ? WHERE name = ?";
                    try (PreparedStatement updateStmt = conn.prepareStatement(updateSql)) {
                        updateStmt.setString(1, updatedMembers);
                        updateStmt.setString(2, projectName);
                        return updateStmt.executeUpdate() > 0;
                    }
                }
            }
        }
        return false;
    }
}
