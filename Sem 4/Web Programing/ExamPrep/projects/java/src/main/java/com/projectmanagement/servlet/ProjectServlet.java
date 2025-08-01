package com.projectmanagement.servlet;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.projectmanagement.dao.ProjectDAO;
import com.projectmanagement.dao.SoftwareDeveloperDAO;
import com.projectmanagement.model.Project;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/api/projects")
public class ProjectServlet extends HttpServlet {
    
    private ProjectDAO projectDAO;
    private SoftwareDeveloperDAO developerDAO;
    private Gson gson;
    
    @Override
    public void init() throws ServletException {
        projectDAO = new ProjectDAO();
        developerDAO = new SoftwareDeveloperDAO();
        gson = new Gson();
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        response.setHeader("Access-Control-Allow-Origin", "*");
        
        PrintWriter out = response.getWriter();
        
        try {
            List<Project> projects = projectDAO.getAllProjects();
            String jsonResponse = gson.toJson(projects);
            out.print(jsonResponse);
            response.setStatus(HttpServletResponse.SC_OK);
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Database error: " + e.getMessage());
            out.print(gson.toJson(error));
        } finally {
            out.close();
        }
    }
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("application/json");
        response.setCharacterEncoding("UTF-8");
        response.setHeader("Access-Control-Allow-Origin", "*");
        
        PrintWriter out = response.getWriter();
        
        try {
            // Read JSON from request body
            StringBuilder jsonBuffer = new StringBuilder();
            BufferedReader reader = request.getReader();
            String line;
            while ((line = reader.readLine()) != null) {
                jsonBuffer.append(line);
            }
            
            JsonObject requestData = gson.fromJson(jsonBuffer.toString(), JsonObject.class);
            String action = requestData.get("action").getAsString();
            
            switch (action) {
                case "get_user_projects":
                    handleGetUserProjects(requestData, response, out);
                    break;
                case "assign_developer":
                    handleAssignDeveloper(requestData, response, out);
                    break;
                default:
                    response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                    JsonObject error = new JsonObject();
                    error.addProperty("message", "Invalid action");
                    out.print(gson.toJson(error));
                    break;
            }
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Server error: " + e.getMessage());
            out.print(gson.toJson(error));
        } finally {
            out.close();
        }
    }
    
    private void handleGetUserProjects(JsonObject requestData, HttpServletResponse response, PrintWriter out) {
        try {
            String username = requestData.get("username").getAsString();
            
            if (username == null || username.trim().isEmpty()) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                JsonObject error = new JsonObject();
                error.addProperty("message", "Username is required");
                out.print(gson.toJson(error));
                return;
            }
            
            List<Project> projects = projectDAO.getProjectsByMember(username);
            List<Map<String, Object>> result = new ArrayList<>();
            
            for (Project project : projects) {
                Map<String, Object> projectMap = new HashMap<>();
                projectMap.put("id", project.getId());
                projectMap.put("name", project.getName());
                result.add(projectMap);
            }
            
            response.setStatus(HttpServletResponse.SC_OK);
            out.print(gson.toJson(result));
            
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Database error: " + e.getMessage());
            out.print(gson.toJson(error));
        }
    }
    
    private void handleAssignDeveloper(JsonObject requestData, HttpServletResponse response, PrintWriter out) {
        try {
            String developer = requestData.get("developer").getAsString();
            
            if (developer == null || developer.trim().isEmpty()) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                JsonObject error = new JsonObject();
                error.addProperty("message", "Developer name is required");
                out.print(gson.toJson(error));
                return;
            }
            
            // Check if developer exists
            if (!developerDAO.developerExists(developer)) {
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                JsonObject error = new JsonObject();
                error.addProperty("message", "Developer does not exist");
                out.print(gson.toJson(error));
                return;
            }
            
            // Get projects array
            List<String> projects = new ArrayList<>();
            requestData.getAsJsonArray("projects").forEach(element -> 
                projects.add(element.getAsString()));
            
            List<Map<String, String>> results = new ArrayList<>();
            
            for (String projectName : projects) {
                Map<String, String> result = new HashMap<>();
                result.put("project", projectName);
                
                // Check if project exists
                if (!projectDAO.projectExists(projectName)) {
                    // Create new project
                    Project newProject = new Project();
                    newProject.setName(projectName);
                    newProject.setDescription("");
                    newProject.setMembers(developer);
                    newProject.setProjectManagerID(0);
                    
                    if (projectDAO.createProject(newProject)) {
                        result.put("status", "created and developer assigned");
                    } else {
                        result.put("status", "failed to create project");
                    }
                } else {
                    // Update existing project
                    if (projectDAO.updateProjectMembers(projectName, developer)) {
                        result.put("status", "developer assigned");
                    } else {
                        result.put("status", "developer already assigned or error occurred");
                    }
                }
                
                results.add(result);
            }
            
            Map<String, Object> responseMap = new HashMap<>();
            responseMap.put("results", results);
            
            response.setStatus(HttpServletResponse.SC_OK);
            out.print(gson.toJson(responseMap));
            
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Database error: " + e.getMessage());
            out.print(gson.toJson(error));
        }
    }
    
    @Override
    protected void doOptions(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
        response.setStatus(HttpServletResponse.SC_OK);
    }
}
