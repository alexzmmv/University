package com.projectmanagement.model;

public class SoftwareDeveloper {
    private int id;
    private String name;
    private int age;
    private String skills;
    
    // Default constructor
    public SoftwareDeveloper() {}
    
    // Constructor with parameters
    public SoftwareDeveloper(String name, int age, String skills) {
        this.name = name;
        this.age = age;
        this.skills = skills;
    }
    
    // Constructor with all fields
    public SoftwareDeveloper(int id, String name, int age, String skills) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.skills = skills;
    }
    
    // Getters and Setters
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
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        this.age = age;
    }
    
    public String getSkills() {
        return skills;
    }
    
    public void setSkills(String skills) {
        this.skills = skills;
    }
    
    @Override
    public String toString() {
        return "SoftwareDeveloper{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                ", skills='" + skills + '\'' +
                '}';
    }
}
