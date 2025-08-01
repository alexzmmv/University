package com.routeapp.model;

public class City {
    private int id;
    private String name;
    private String country;
    private int distance;
    public City() {}
    
    public City(String name, String country) {
        this.name = name;
        this.country = country;
    }
    
    public City(int id, String name, String country) {
        this.id = id;
        this.name = name;
        this.country = country;
    }


    public City(int id, String name, String country, int distance) {
        this.id = id;
        this.name = name;
        this.country = country;
        this.distance = distance;
    }
    
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getCountry() {
        return country;
    }
    
    public void setCountry(String country) {
        this.country = country;
    }
    
    public int getDistance() {
        return distance;
    }

    public void setDistance(int distance) {
        this.distance = distance;
    }
    @Override
    public String toString() {
        return name + ", " + country;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        City city = (City) obj;
        return id == city.id;
    }
    
    @Override
    public int hashCode() {
        return Integer.hashCode(id);
    }
}