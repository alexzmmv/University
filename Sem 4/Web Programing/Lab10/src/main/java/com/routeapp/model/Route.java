package com.routeapp.model;

import java.util.ArrayList;
import java.util.List;

public class Route {
    private List<City> cities;
    private int totalDistance;
    
    public Route() {
        this.cities = new ArrayList<>();
        this.totalDistance = 0;
    }
    
    public Route(List<City> cities) {
        this.cities = new ArrayList<>(cities);
        this.totalDistance = 0;
    }
    
    public void addCity(City city) {
        if (cities == null) {
            cities = new ArrayList<>();
        }
        cities.add(city);
    }
    
    public void removeLastCity() {
        if (cities != null && !cities.isEmpty()) {
            cities.remove(cities.size() - 1);
        }
    }
    
    public City getCurrentCity() {
        if (cities == null || cities.isEmpty()) {
            return null;
        }
        return cities.get(cities.size() - 1);
    }
    
    public City getPreviousCity() {
        if (cities == null || cities.size() < 2) {
            return null;
        }
        return cities.get(cities.size() - 2);
    }
    
    public boolean canGoBack() {
        return cities != null && cities.size() > 1;
    }
    
    public void goBackTo(int cityIndex) {
        if (cities != null && cityIndex >= 0 && cityIndex < cities.size()) {
            cities = cities.subList(0, cityIndex + 1);
        }
    }
    
    public List<City> getCities() {
        return cities;
    }
    
    public void setCities(List<City> cities) {
        this.cities = cities;
    }
    
    public int getTotalDistance() {
        return totalDistance;
    }
    
    public void setTotalDistance(int totalDistance) {
        this.totalDistance = totalDistance;
    }
    
    public int size() {
        return cities == null ? 0 : cities.size();
    }
    
    public boolean isEmpty() {
        return cities == null || cities.isEmpty();
    }
    
    public void clear() {
        if (cities != null) {
            cities.clear();
        }
        totalDistance = 0;
    }
}
