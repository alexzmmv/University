<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transportation Route App - Route Selection</title>
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
                <a href="${pageContext.request.contextPath}/logout" 
                   id="logoutBtn" 
                   class="btn btn-secondary btn-sm">
                    Logout
                </a>
            </div>
        </div>
        
        <!-- Page Header -->
        <div class="header">
            <h1>🚌 Transportation Route Planner</h1>
            <p>Plan your journey by selecting connected cities</p>
        </div>
        
        <div class="content">
            <!-- Display messages -->
            <c:if test="${not empty message}">
                <div class="alert alert-success">
                    ${message}
                </div>
            </c:if>
            
            <c:if test="${not empty error}">
                <div class="alert alert-error">
                    ${error}
                </div>
            </c:if>
            
            <!-- Current Station Display -->
            <div class="current-station">
                <h3>Current Station</h3>
                <c:choose>
                    <c:when test="${empty currentCity}">
                        <div class="station-name">🏁 Select your starting city</div>
                        <p>Choose any city below to begin your journey</p>
                    </c:when>
                    <c:otherwise>
                        <div class="station-name">📍 ${currentCity.name}, ${currentCity.country}</div>
                        <p>Select your next destination from the connected cities below</p>
                    </c:otherwise>
                </c:choose>
            </div>
            
            <!-- Route History -->
            <c:if test="${not empty route.cities and route.cities.size() > 0}">
                <div class="route-history">
                    <h3>🛤️ Your Route So Far</h3>
                    <c:forEach var="city" items="${route.cities}" varStatus="status">
                        <div class="history-item">
                            <span class="history-city">
                                ${status.index + 1}. ${city.name}, ${city.country}
                            </span>
                            <div class="history-actions">
                                <c:if test="${status.index < route.cities.size() - 1}">
                                    <button type="button" 
                                            class="btn btn-warning btn-sm back-to-btn"
                                            data-index="${status.index}"
                                            data-city-name="${city.name}">
                                        Go Back Here
                                    </button>
                                </c:if>
                            </div>
                        </div>
                    </c:forEach>
                    
                    <div style="margin-top: 15px; padding: 10px; background: #1a1a2e; border-radius: 6px; text-align: center; border: 2px solid #87ceeb;">
                        <strong style="color: #87ceeb;">Total Distance: ${route.totalDistance} km</strong>
                    </div>
                </div>
            </c:if>
            
            <!-- Available Cities -->
            <div style="margin-bottom: 25px;">
                <h3>
                    <c:choose>
                        <c:when test="${empty currentCity}">
                            🌍 Available Starting Cities
                        </c:when>
                        <c:otherwise>
                            🚌 Connected Destinations from ${currentCity.name}
                        </c:otherwise>
                    </c:choose>
                </h3>
                
                <c:choose>
                    <c:when test="${empty connectedCities}">
                        <div class="alert alert-info">
                            <c:choose>
                                <c:when test="${empty currentCity}">
                                    No cities available to start your journey.
                                </c:when>
                                <c:otherwise>
                                    No direct connections available from ${currentCity.name}. 
                                    You can finish your route or go back to a previous city.
                                </c:otherwise>
                            </c:choose>
                        </div>
                    </c:when>
                    <c:otherwise>
                        <div class="cities-grid">
                            <c:forEach var="city" items="${connectedCities}">
                                <div class="city-card" data-city-id="${city.id}">
                                    <h4>${city.name}</h4>
                                    <p>${city.country}</p>
                                    <p>Distance: ${city.distance} km</p>
                                    <button type="button" class="btn btn-primary btn-sm">
                                        <c:choose>
                                            <c:when test="${empty currentCity}">
                                                Start Here
                                            </c:when>
                                            <c:otherwise>
                                                Go to ${city.name}
                                            </c:otherwise>
                                        </c:choose>
                                    </button>
                                </div>
                            </c:forEach>
                        </div>
                    </c:otherwise>
                </c:choose>
            </div>
            
            <!-- Route Actions -->
            <div class="route-actions">
                <c:if test="${not empty route.cities and route.cities.size() > 0}">
                    <button type="button" id="goBackBtn" class="btn btn-secondary">
                        ⬅️ Go Back One Step
                    </button>
                    
                    <form style="display: inline;" action="${pageContext.request.contextPath}/route/route" method="post">
                        <input type="hidden" name="action" value="finishRoute">
                        <button type="submit" class="btn btn-success">
                            🏁 Finish Route
                        </button>
                    </form>
                    
                    <button type="button" id="clearRouteBtn" class="btn btn-danger">
                        🗑️ Clear Route
                    </button>
                </c:if>
                
                <c:if test="${empty route.cities or route.cities.size() == 0}">
                    <p style="color: #87ceeb; font-style: italic;">
                        Select a starting city to begin planning your route
                    </p>
                </c:if>
            </div>
        </div>
    </div>
    
    <script src="${pageContext.request.contextPath}/js/app.js"></script>
</body>
</html>
