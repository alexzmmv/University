<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transportation Route App - Login</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <div class="login-container">
        <div class="login-form">
            <div class="login-header">
                <h2 id="formTitle">Login</h2>
                <p>Enter your credentials to access the route planning system</p>
            </div>
            
            <c:if test="${not empty error}">
                <div class="alert alert-error">
                    ${error}
                </div>
            </c:if>
            
            <c:if test="${not empty success}">
                <div class="alert alert-success">
                    ${success}
                </div>
            </c:if>
            
            <c:if test="${param.message == 'logout'}">
                <div class="alert alert-info">
                    You have been successfully logged out.
                </div>
            </c:if>
            
            <form id="loginForm" action="${pageContext.request.contextPath}/login" method="post">
                <input type="hidden" id="action" name="action" value="login">
                
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" 
                           id="username" 
                           name="username" 
                           class="form-control" 
                           placeholder="Enter your username"
                           value="${param.username}"
                           required
                           autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" 
                           id="password" 
                           name="password" 
                           class="form-control" 
                           placeholder="Enter your password"
                           required
                           autocomplete="current-password">
                </div>
                
                <button type="submit" id="submitBtn" class="btn btn-primary btn-block">
                    Login
                </button>
            </form>
            
            <div class="form-toggle">
                <a href="#" id="toggleForm">Don't have an account? Register here</a>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #444; font-size: 14px; color: #aaa;">
                <strong style="color: #ccc;">Demo Credentials:</strong><br>
                Username: <code style="background: #333; color: #e0e0e0; padding: 2px 4px; border-radius: 3px;">admin</code> or <code style="background: #333; color: #e0e0e0; padding: 2px 4px; border-radius: 3px;">user1</code><br>
                Password: <code style="background: #333; color: #e0e0e0; padding: 2px 4px; border-radius: 3px;">admin123</code>
            </div>
        </div>
    </div>
    
    <script src="${pageContext.request.contextPath}/js/app.js"></script>
</body>
</html>
