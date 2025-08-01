package com.routeapp.servlets;

import com.routeapp.dao.CityDAO;
import com.routeapp.model.City;
import com.routeapp.model.Route;
import com.routeapp.util.DatabaseUtil;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.List;

public class RouteServlet extends HttpServlet {
    private CityDAO cityDAO;
    
    @Override
    public void init(ServletConfig config) throws ServletException {
        super.init(config);
        DatabaseUtil.init(getServletContext());
        cityDAO = new CityDAO();
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String pathInfo = request.getPathInfo();
        HttpSession session = request.getSession();
        
        if (pathInfo == null || pathInfo.equals("/") || pathInfo.equals("/select")) {
            handleCitySelection(request, response, session);
        } else if (pathInfo.equals("/route")) {
            handleRouteDisplay(request, response, session);
        } else {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
        }
    }
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String pathInfo = request.getPathInfo();
        HttpSession session = request.getSession();
        
        if (pathInfo == null || pathInfo.equals("/") || pathInfo.equals("/select")) {
            handleCitySelectionPost(request, response, session);
        } else if (pathInfo.equals("/route")) {
            handleRouteAction(request, response, session);
        } else {
            response.sendError(HttpServletResponse.SC_NOT_FOUND);
        }
    }
    
    private void handleCitySelection(HttpServletRequest request, HttpServletResponse response, HttpSession session)
            throws ServletException, IOException {
        
        Route route = (Route) session.getAttribute("route");
        if (route == null) {
            route = new Route();
            session.setAttribute("route", route);
        }
        
        City currentCity = route.getCurrentCity();
        List<City> connectedCities = null;
        
        if (currentCity != null) {
            connectedCities = cityDAO.getConnectedCities(currentCity.getId());
        } else {
            // If no current city, show all cities to start
            connectedCities = cityDAO.getAllCities();
        }
        
        request.setAttribute("currentCity", currentCity);
        request.setAttribute("connectedCities", connectedCities);
        request.setAttribute("route", route);
        
        request.getRequestDispatcher("/route-selection.jsp").forward(request, response);
    }
    
    private void handleCitySelectionPost(HttpServletRequest request, HttpServletResponse response, HttpSession session)
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        String cityIdStr = request.getParameter("cityId");
        String backToIndexStr = request.getParameter("backToIndex");
        
        Route route = (Route) session.getAttribute("route");
        if (route == null) {
            route = new Route();
            session.setAttribute("route", route);
        }
        
        try {
            if ("selectCity".equals(action) && cityIdStr != null) {
                int cityId = Integer.parseInt(cityIdStr);
                City selectedCity = cityDAO.getCityById(cityId);
                
                if (selectedCity != null) {
                    // Calculate distance if there's a previous city
                    if (route.getCurrentCity() != null) {
                        int distance = cityDAO.getDistance(route.getCurrentCity().getId(), selectedCity.getId());
                        route.setTotalDistance(route.getTotalDistance() + distance);
                    }
                    
                    route.addCity(selectedCity);
                    request.setAttribute("message", "Added " + selectedCity + " to your route.");
                }
            } else if ("goBack".equals(action)) {
                if (route.canGoBack()) {
                    route.removeLastCity();
                    // Recalculate total distance
                    recalculateDistance(route);
                    request.setAttribute("message", "Went back one step in your route.");
                }
            } else if ("backTo".equals(action) && backToIndexStr != null) {
                int backToIndex = Integer.parseInt(backToIndexStr);
                route.goBackTo(backToIndex);
                // Recalculate total distance
                recalculateDistance(route);
                request.setAttribute("message", "Went back to selected city.");
            } else if ("clearRoute".equals(action)) {
                route.clear();
                request.setAttribute("message", "Route cleared.");
            } else if ("finishRoute".equals(action)) {
                if (!route.isEmpty()) {
                    response.sendRedirect(request.getContextPath() + "/route/route");
                    return;
                }
            }
        } catch (NumberFormatException e) {
            request.setAttribute("error", "Invalid city selection.");
        }
        
        // Redirect to avoid form resubmission
        response.sendRedirect(request.getContextPath() + "/route/select");
    }
    
    private void handleRouteDisplay(HttpServletRequest request, HttpServletResponse response, HttpSession session)
            throws ServletException, IOException {
        
        Route route = (Route) session.getAttribute("route");
        if (route == null || route.isEmpty()) {
            response.sendRedirect(request.getContextPath() + "/route/select");
            return;
        }
        
        request.setAttribute("route", route);
        request.getRequestDispatcher("/route-display.jsp").forward(request, response);
    }
    
    private void handleRouteAction(HttpServletRequest request, HttpServletResponse response, HttpSession session)
            throws ServletException, IOException {
        
        String action = request.getParameter("action");
        Route route = (Route) session.getAttribute("route");
        
        if ("newRoute".equals(action)) {
            if (route != null) {
                route.clear();
            }
            response.sendRedirect(request.getContextPath() + "/route/select");
        } else {
            response.sendRedirect(request.getContextPath() + "/route/route");
        }
    }
    
    private void recalculateDistance(Route route) {
        if (route == null || route.size() < 2) {
            route.setTotalDistance(0);
            return;
        }
        
        int totalDistance = 0;
        List<City> cities = route.getCities();
        
        for (int i = 1; i < cities.size(); i++) {
            City fromCity = cities.get(i - 1);
            City toCity = cities.get(i);
            int distance = cityDAO.getDistance(fromCity.getId(), toCity.getId());
            totalDistance += distance;
        }
        
        route.setTotalDistance(totalDistance);
    }
}
