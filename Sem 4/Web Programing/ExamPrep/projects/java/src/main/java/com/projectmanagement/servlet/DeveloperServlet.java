package com.projectmanagement.servlet;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.projectmanagement.dao.SoftwareDeveloperDAO;
import com.projectmanagement.model.SoftwareDeveloper;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@WebServlet("/api/developers")
public class DeveloperServlet extends HttpServlet {
    
    private SoftwareDeveloperDAO developerDAO;
    private Gson gson;
    
    @Override
    public void init() throws ServletException {
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
            List<SoftwareDeveloper> developers = developerDAO.getAllDevelopers();
            String jsonResponse = gson.toJson(developers);
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
            
            if (requestData.has("action") && 
                "check_user".equals(requestData.get("action").getAsString())) {
                
                // Check if user exists
                String username = requestData.get("username").getAsString();
                
                if (username == null || username.trim().isEmpty()) {
                    response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                    JsonObject error = new JsonObject();
                    error.addProperty("message", "Username is required");
                    out.print(gson.toJson(error));
                    return;
                }
                
                boolean exists = developerDAO.developerExists(username);
                Map<String, Boolean> result = new HashMap<>();
                result.put("exists", exists);
                
                response.setStatus(HttpServletResponse.SC_OK);
                out.print(gson.toJson(result));
                
            } else {
                // Create new developer
                String name = requestData.get("name").getAsString();
                
                if (name == null || name.trim().isEmpty()) {
                    response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                    JsonObject error = new JsonObject();
                    error.addProperty("message", "Name is required");
                    out.print(gson.toJson(error));
                    return;
                }
                
                SoftwareDeveloper developer = new SoftwareDeveloper();
                developer.setName(name);
                
                if (requestData.has("age") && !requestData.get("age").isJsonNull()) {
                    developer.setAge(requestData.get("age").getAsInt());
                }
                
                if (requestData.has("skills") && !requestData.get("skills").isJsonNull()) {
                    developer.setSkills(requestData.get("skills").getAsString());
                } else {
                    developer.setSkills("");
                }
                
                if (developerDAO.createDeveloper(developer)) {
                    response.setStatus(HttpServletResponse.SC_CREATED);
                    JsonObject success = new JsonObject();
                    success.addProperty("message", "Developer created successfully");
                    out.print(gson.toJson(success));
                } else {
                    response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
                    JsonObject error = new JsonObject();
                    error.addProperty("message", "Unable to create developer");
                    out.print(gson.toJson(error));
                }
            }
            
        } catch (SQLException e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Database error: " + e.getMessage());
            out.print(gson.toJson(error));
        } catch (Exception e) {
            response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
            JsonObject error = new JsonObject();
            error.addProperty("message", "Server error: " + e.getMessage());
            out.print(gson.toJson(error));
        } finally {
            out.close();
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
