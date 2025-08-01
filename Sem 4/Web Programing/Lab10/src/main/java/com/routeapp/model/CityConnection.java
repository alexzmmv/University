package com.routeapp.model;

public class CityConnection {
    private int id;
    private int fromCityId;
    private int toCityId;
    private int distance;
    private City fromCity;
    private City toCity;
    
    public CityConnection() {}
    
    public CityConnection(int fromCityId, int toCityId, int distance) {
        this.fromCityId = fromCityId;
        this.toCityId = toCityId;
        this.distance = distance;
    }
    
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public int getFromCityId() {
        return fromCityId;
    }
    
    public void setFromCityId(int fromCityId) {
        this.fromCityId = fromCityId;
    }
    
    public int getToCityId() {
        return toCityId;
    }
    
    public void setToCityId(int toCityId) {
        this.toCityId = toCityId;
    }
    
    public int getDistance() {
        return distance;
    }
    
    public void setDistance(int distance) {
        this.distance = distance;
    }
    
    public City getFromCity() {
        return fromCity;
    }
    
    public void setFromCity(City fromCity) {
        this.fromCity = fromCity;
    }
    
    public City getToCity() {
        return toCity;
    }
    
    public void setToCity(City toCity) {
        this.toCity = toCity;
    }
}
