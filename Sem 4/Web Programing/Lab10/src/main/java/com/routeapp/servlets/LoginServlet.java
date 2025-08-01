package com.routeapp.servlets;

import com.routeapp.dao.UserDAO;
import com.routeapp.model.User;
import com.routeapp.util.DatabaseUtil;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;

public class LoginServlet extends HttpServlet {
    private UserDAO userDAO;
    
    @Override
    public void init(ServletConfig config) throws ServletException {
        super.init(config);
        DatabaseUtil.init(getServletContext());
        userDAO = new UserDAO();
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect(request.getContextPath() + "/login.jsp");
    }
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        String action = request.getParameter("action");
        
        if (username == null || username.trim().isEmpty() || 
            password == null || password.trim().isEmpty()) {
            request.setAttribute("error", "Username and password are required");
            request.getRequestDispatcher("/login.jsp").forward(request, response);
            return;
        }
        
        username = username.trim();
        
        if (!username.matches("^[a-zA-Z0-9_]{3,20}$")) {
            request.setAttribute("error", "Username must be 3-20 characters long and contain only letters, numbers, and underscores");
            request.getRequestDispatcher("/login.jsp").forward(request, response);
            return;
        }
        
        if (password.length() < 6 || password.length() > 20) {
            request.setAttribute("error", "Password must be 6-20 characters long");
            request.getRequestDispatcher("/login.jsp").forward(request, response);
            return;
        }
        
        try {
            if ("register".equals(action)) {
                if (userDAO.userExists(username)) {
                    request.setAttribute("error", "Username already exists");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                    return;
                }
                
                if (userDAO.createUser(username, password)) {
                    request.setAttribute("success", "Registration successful! Please login.");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                } else {
                    request.setAttribute("error", "Registration failed. Please try again.");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                }
            } else 
            {
                User user = userDAO.authenticate(username, password);
                boolean AuthenticationSuccessful = (user != null);
                if (AuthenticationSuccessful) {
                    HttpSession session = request.getSession(true);
                    session.setAttribute("user", user);
                    session.setAttribute("username", user.getUsername());
                    session.setMaxInactiveInterval(30 * 60);
                    
                    response.sendRedirect(request.getContextPath() + "/route/select");
                } else {
                    request.setAttribute("error", "Invalid username or password");
                    request.getRequestDispatcher("/login.jsp").forward(request, response);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("error", "An error occurred. Please try again.");
            request.getRequestDispatcher("/login.jsp").forward(request, response);
        }
    }
}
