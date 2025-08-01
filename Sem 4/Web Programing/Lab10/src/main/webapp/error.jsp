<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transportation Route App - Error</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ Oops! Something went wrong</h1>
            <p>We encountered an unexpected error</p>
        </div>
        
        <div class="content">
            <div class="alert alert-error">
                <h3>Error Details</h3>
                <c:choose>
                    <c:when test="${not empty pageContext.exception}">
                        <p><strong>Error:</strong> ${pageContext.exception.message}</p>
                        <p><strong>Type:</strong> ${pageContext.exception.class.simpleName}</p>
                    </c:when>
                    <c:when test="${not empty requestScope['javax.servlet.error.message']}">
                        <p><strong>Error:</strong> ${requestScope['javax.servlet.error.message']}</p>
                    </c:when>
                    <c:when test="${not empty requestScope['javax.servlet.error.status_code']}">
                        <p><strong>Status Code:</strong> ${requestScope['javax.servlet.error.status_code']}</p>
                        <c:choose>
                            <c:when test="${requestScope['javax.servlet.error.status_code'] == 404}">
                                <p>The page you requested could not be found.</p>
                            </c:when>
                            <c:when test="${requestScope['javax.servlet.error.status_code'] == 500}">
                                <p>An internal server error occurred.</p>
                            </c:when>
                            <c:otherwise>
                                <p>An unexpected error occurred.</p>
                            </c:otherwise>
                        </c:choose>
                    </c:when>
                    <c:otherwise>
                        <p>An unknown error occurred. Please try again.</p>
                    </c:otherwise>
                </c:choose>
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <a href="${pageContext.request.contextPath}/route/select" class="btn btn-primary">
                    🏠 Go to Home
                </a>
                
                <button type="button" onclick="history.back()" class="btn btn-secondary">
                    ⬅️ Go Back
                </button>
                
                <button type="button" onclick="location.reload()" class="btn btn-secondary">
                    🔄 Refresh Page
                </button>
            </div>
            
            <div style="margin-top: 40px; padding: 20px; background: #2a2a2a; border-radius: 8px; border: 1px solid #444;">
                <h4 style="color: #e0e0e0;">💡 What you can do:</h4>
                <ul style="margin-top: 15px; padding-left: 20px; color: #ccc;">
                    <li>Check if the URL is correct</li>
                    <li>Try refreshing the page</li>
                    <li>Go back to the previous page</li>
                    <li>Return to the home page and try again</li>
                    <li>If the problem persists, please contact support</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script src="${pageContext.request.contextPath}/js/app.js"></script>
</body>
</html>
