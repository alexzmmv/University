<%@ page contentType="text/html;charset=UTF-8" language="java" isErrorPage="true" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error - Project Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
            text-align: center;
        }
        .error-container {
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .error-code {
            font-size: 72px;
            color: #e74c3c;
            margin-bottom: 20px;
        }
        .error-message {
            font-size: 24px;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .back-link {
            background-color: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 4px;
            display: inline-block;
        }
        .back-link:hover {
            background-color: #2980b9;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">
            <% 
                Integer errorCode = (Integer) request.getAttribute("javax.servlet.error.status_code");
                if (errorCode != null) {
                    out.print(errorCode);
                } else {
                    out.print("500");
                }
            %>
        </div>
        
        <div class="error-message">
            <% 
                if (errorCode != null && errorCode == 404) {
                    out.print("Page Not Found");
                } else {
                    out.print("Internal Server Error");
                }
            %>
        </div>
        
        <p>
            <% 
                if (errorCode != null && errorCode == 404) {
                    out.print("The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.");
                } else {
                    out.print("Something went wrong on our end. Please try again later or contact the administrator.");
                }
            %>
        </p>
        
        <a href="<%= request.getContextPath() %>/" class="back-link">← Back to Home</a>
    </div>
</body>
</html>
