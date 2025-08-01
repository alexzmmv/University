package com.routeapp.dao;

import com.routeapp.model.City;
import com.routeapp.model.CityConnection;
import com.routeapp.util.DatabaseUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CityDAO {
    
    public List<City> getAllCities() {
        List<City> cities = new ArrayList<>();
        String sql = "SELECT id, name, country FROM cities ORDER BY name";
        
        try (Connection connection = DatabaseUtil.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            
            while (resultSet.next()) {
                City city = new City(
                    resultSet.getInt("id"),
                    resultSet.getString("name"),
                    resultSet.getString("country")
                );
                city.setDistance(0);
                cities.add(city);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return cities;
    }
    
    public City getCityById(int id) {
        String sql = "SELECT id, name, country FROM cities WHERE id = ?";
        
        try (Connection connection = DatabaseUtil.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            
            statement.setInt(1, id);
            ResultSet resultSet = statement.executeQuery();
            
            if (resultSet.next()) {
                City city = new City(
                    resultSet.getInt("id"),
                    resultSet.getString("name"),
                    resultSet.getString("country")
                );
                city.setDistance(0);
                return city;
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return null;
    }
    
    public List<City> getConnectedCities(int cityId) {
        List<City> connectedCities = new ArrayList<>();
        String sql = "SELECT c.id, c.name, c.country, cc.distance " +
                    "FROM cities c " +
                    "INNER JOIN city_connections cc ON c.id = cc.to_city_id " +
                    "WHERE cc.from_city_id = ? " +
                    "ORDER BY c.name";
        
        try (Connection connection = DatabaseUtil.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            
            statement.setInt(1, cityId);
            ResultSet resultSet = statement.executeQuery();
            
            while (resultSet.next()) {
                City city = new City(
                    resultSet.getInt("id"),
                    resultSet.getString("name"),
                    resultSet.getString("country"),
                    resultSet.getInt("distance")
                );
                connectedCities.add(city);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return connectedCities;
    }
    
    public int getDistance(int fromCityId, int toCityId) {
        String sql = "SELECT distance FROM city_connections WHERE from_city_id = ? AND to_city_id = ?";
        
        try (Connection connection = DatabaseUtil.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            
            statement.setInt(1, fromCityId);
            statement.setInt(2, toCityId);
            ResultSet resultSet = statement.executeQuery();
            
            if (resultSet.next()) {
                return resultSet.getInt("distance");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return 0;
    }
    
    public List<CityConnection> getAllConnections() {
        List<CityConnection> connections = new ArrayList<>();
        String sql = "SELECT cc.id, cc.from_city_id, cc.to_city_id, cc.distance, " +
                    "cf.name as from_name, cf.country as from_country, " +
                    "ct.name as to_name, ct.country as to_country " +
                    "FROM city_connections cc " +
                    "INNER JOIN cities cf ON cc.from_city_id = cf.id " +
                    "INNER JOIN cities ct ON cc.to_city_id = ct.id " +
                    "ORDER BY cf.name, ct.name";
        
        try (Connection connection = DatabaseUtil.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            
            while (resultSet.next()) {
                CityConnection cityConnection = new CityConnection();
                cityConnection.setId(resultSet.getInt("id"));
                cityConnection.setFromCityId(resultSet.getInt("from_city_id"));
                cityConnection.setToCityId(resultSet.getInt("to_city_id"));
                cityConnection.setDistance(resultSet.getInt("distance"));
                
                City fromCity = new City(
                    resultSet.getInt("from_city_id"),
                    resultSet.getString("from_name"),
                    resultSet.getString("from_country")
                );
                fromCity.setDistance(0);
                
                City toCity = new City(
                    resultSet.getInt("to_city_id"),
                    resultSet.getString("to_name"),
                    resultSet.getString("to_country")
                );
                toCity.setDistance(0);

                cityConnection.setFromCity(fromCity);
                cityConnection.setToCity(toCity);
                connections.add(cityConnection);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return connections;
    }
}