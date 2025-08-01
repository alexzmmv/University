package com.projectmanagement.servlet;

import com.projectmanagement.config.DatabaseConfig;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.Statement;

@WebServlet("/setup-database")
public class DatabaseSetupServlet extends HttpServlet {
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("text/html");
        response.setCharacterEncoding("UTF-8");
        
        PrintWriter out = response.getWriter();
        
        try {
            setupDatabase();
            
            out.println("<!DOCTYPE html>");
            out.println("<html><head><title>Database Setup</title></head><body>");
            out.println("<h1>✅ Database Setup Successful!</h1>");
            out.println("<p>Database and tables created successfully with sample data.</p>");
            out.println("<p><a href='index.jsp'>Go to Application</a></p>");
            out.println("</body></html>");
            
        } catch (Exception e) {
            out.println("<!DOCTYPE html>");
            out.println("<html><head><title>Database Setup Error</title></head><body>");
            out.println("<h1>❌ Database Setup Failed!</h1>");
            out.println("<p>Error: " + e.getMessage() + "</p>");
            out.println("<p>Please check your database configuration.</p>");
            out.println("</body></html>");
        } finally {
            out.close();
        }
    }
    
    private void setupDatabase() throws Exception {
        try (Connection conn = DatabaseConfig.getConnection();
             Statement stmt = conn.createStatement()) {
            
            // Create SoftwareDeveloper table
            String createDeveloperTable = 
                "CREATE TABLE IF NOT EXISTS SoftwareDeveloper (" +
                "id INT AUTO_INCREMENT PRIMARY KEY," +
                "name VARCHAR(255) NOT NULL," +
                "age INT," +
                "skills TEXT" +
                ")";
            stmt.executeUpdate(createDeveloperTable);
            
            // Create Project table
            String createProjectTable = 
                "CREATE TABLE IF NOT EXISTS Project (" +
                "id INT AUTO_INCREMENT PRIMARY KEY," +
                "ProjectManagerID INT," +
                "name VARCHAR(255) NOT NULL," +
                "description TEXT," +
                "members TEXT," +
                "FOREIGN KEY (ProjectManagerID) REFERENCES SoftwareDeveloper(id)" +
                ")";
            stmt.executeUpdate(createProjectTable);
            
            // Insert sample developers
            String insertDevelopers = 
                "INSERT IGNORE INTO SoftwareDeveloper (id, name, age, skills) VALUES " +
                "(1, 'John Doe', 30, 'Java, Python, SQL')," +
                "(2, 'Jane Smith', 28, 'PHP, JavaScript, HTML')," +
                "(3, 'Mike Johnson', 35, 'C#, .NET, SQL')," +
                "(4, 'Sarah Wilson', 26, 'Java, Spring, React')," +
                "(5, 'David Brown', 32, 'Python, Django, PostgreSQL')";
            stmt.executeUpdate(insertDevelopers);
            
            // Insert sample projects
            String insertProjects = 
                "INSERT IGNORE INTO Project (id, ProjectManagerID, name, description, members) VALUES " +
                "(1, 1, 'E-commerce Platform', 'Online shopping platform', 'John Doe, Jane Smith')," +
                "(2, 2, 'Mobile App', 'iOS and Android mobile application', 'Jane Smith, Mike Johnson, Sarah Wilson')," +
                "(3, 3, 'Data Analytics Tool', 'Business intelligence dashboard', 'Mike Johnson, David Brown')";
            stmt.executeUpdate(insertProjects);
        }
    }
}
