<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transportation Route App - Your Route</title>
    <link rel="stylesheet" href="${pageContext.request.contextPath}/css/style.css">
</head>
<body>
    <div class="container">
        <!-- Navigation Header -->
        <div class="nav">
            <div class="nav-user">
                Welcome, <strong>${sessionScope.username}</strong>
            </div>
            <div>
                <a href="${pageContext.request.contextPath}/route/select" class="btn btn-secondary btn-sm">
                    ← Back to Planning
                </a>
                <a href="${pageContext.request.contextPath}/logout" 
                   id="logoutBtn" 
                   class="btn btn-secondary btn-sm">
                    Logout
                </a>
            </div>
        </div>
        
        <!-- Page Header -->
        <div class="header">
            <h1>🗺️ Your Complete Route</h1>
            <p>Review your planned journey</p>
        </div>
        
        <div class="content">
            <c:choose>
                <c:when test="${empty route or empty route.cities or route.cities.size() == 0}">
                    <div class="alert alert-info">
                        <h3>No Route Available</h3>
                        <p>You haven't planned a route yet. Start by selecting your starting city.</p>
                        <a href="${pageContext.request.contextPath}/route/select" class="btn btn-primary">
                            Start Planning
                        </a>
                    </div>
                </c:when>
                <c:otherwise>
                    <!-- Route Summary -->
                    <div class="route-summary">
                        <h3>📊 Route Summary</h3>
                        <div class="total-distance">
                            Total Distance: ${route.totalDistance} km
                        </div>
                        <p style="margin-top: 10px; margin-bottom: 0;">
                            <strong>${route.cities.size()}</strong> cities in your route
                        </p>
                    </div>
                    
                    <!-- Detailed Route Steps -->
                    <div style="margin-bottom: 30px;">
                        <h3>🛤️ Detailed Route</h3>
                        
                        <c:forEach var="city" items="${route.cities}" varStatus="status">
                            <div class="route-step">
                                <div class="step-number">${status.index + 1}</div>
                                <div class="step-info">
                                    <h4>${city.name}, ${city.country}</h4>
                                    <c:choose>
                                        <c:when test="${status.index == 0}">
                                            <p><strong>🏁 Starting Point</strong></p>
                                        </c:when>
                                        <c:when test="${status.index == route.cities.size() - 1}">
                                            <p><strong>🎯 Final Destination</strong></p>
                                        </c:when>
                                        <c:otherwise>
                                            <p>🚌 Transit stop ${status.index}</p>
                                        </c:otherwise>
                                    </c:choose>
                                </div>
                            </div>
                        </c:forEach>
                    </div>
                    
                    <!-- Route Actions -->
                    <div class="route-actions">
                        <a href="${pageContext.request.contextPath}/route/select" class="btn btn-primary">
                            ✏️ Continue Planning
                        </a>
                        
                        <button type="button" id="newRouteBtn" class="btn btn-warning">
                            🔄 Start New Route
                        </button>
                        
                        <button type="button" onclick="window.print()" class="btn btn-secondary">
                            🖨️ Print Route
                        </button>
                        
                        <button type="button" onclick="shareRoute()" class="btn btn-secondary">
                            📤 Share Route
                        </button>
                    </div>
                    
                    <!-- Route Statistics -->
                    <div style="margin-top: 40px; padding: 20px; background: #1a1a2e; border-radius: 8px; border: 2px solid #87ceeb;">
                        <h4 style="color: #87ceeb;">📈 Route Statistics</h4>
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 15px;">
                            <div style="text-align: center;">
                                <div style="font-size: 2em; font-weight: bold; color: #87ceeb;">${route.cities.size()}</div>
                                <div style="color: #e0f4ff;">Cities Visited</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 2em; font-weight: bold; color: #4682b4;">${route.totalDistance}</div>
                                <div style="color: #e0f4ff;">Total Distance (km)</div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 2em; font-weight: bold; color: #87ceeb;">${route.cities.size() - 1}</div>
                                <div style="color: #e0f4ff;">Route Segments</div>
                            </div>
                        </div>
                    </div>
                </c:otherwise>
            </c:choose>
        </div>
    </div>
    
    <script src="${pageContext.request.contextPath}/js/app.js"></script>
    <script>
        function shareRoute() {
            const routeText = generateRouteText();
            
            if (navigator.share) {
                navigator.share({
                    title: 'My Transportation Route',
                    text: routeText,
                    url: window.location.href
                }).catch(console.error);
            } else if (navigator.clipboard) {
                navigator.clipboard.writeText(routeText).then(() => {
                    alert('Route copied to clipboard!');
                }).catch(() => {
                    fallbackCopyTextToClipboard(routeText);
                });
            } else {
                fallbackCopyTextToClipboard(routeText);
            }
        }
        
        function generateRouteText() {
            const cities = [
                <c:forEach var="city" items="${route.cities}" varStatus="status">
                    "${city.name}, ${city.country}"<c:if test="${!status.last}">,</c:if>
                </c:forEach>
            ];
            
            let text = "🗺️ My Transportation Route\\n";
            
            cities.forEach((city, index) => {
                text += `${index + 1}. ${city}\\n`;
            });
            
            text += `📊 Total Distance: ${route.totalDistance} km`;
            text += `🏛️ Cities: ${cities.length}`;
            text += "Generated by Transportation Route App";
            
            return text;
        }
        
        function fallbackCopyTextToClipboard(text) {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            
            textArea.style.top = "0";
            textArea.style.left = "0";
            textArea.style.position = "fixed";
            
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {
                document.execCommand('copy');
                alert('Route copied to clipboard!');
            } catch (err) {
                console.error('Fallback: Oops, unable to copy', err);
                prompt('Copy the route manually:', text);
            }
            
            document.body.removeChild(textArea);
        }
    </script>
    
    <style>
        @media print {
            .nav, .route-actions, .btn {
                display: none !important;
            }
            
            .container {
                box-shadow: none;
                margin: 0;
                background: white !important;
            }
            
            .header {
                background: none !important;
                color: black !important;
                border-bottom: 2px solid #333;
            }
            
            .route-step, .route-summary, .current-station {
                background: white !important;
                color: black !important;
                border: 1px solid #ccc !important;
            }
            
            .route-step::after {
                color: black !important;
            }
            
            .step-number {
                background: #333 !important;
                color: white !important;
            }
            
            .step-info h4, .step-info p {
                color: black !important;
            }
        }
    </style>
</body>
</html>
