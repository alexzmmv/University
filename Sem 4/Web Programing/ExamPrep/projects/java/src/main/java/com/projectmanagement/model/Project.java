package com.projectmanagement.model;

public class Project {
    private int id;
    private int projectManagerID;
    private String name;
    private String description;
    private String members;
    private String managerName; // For display purposes
    
    // Default constructor
    public Project() {}
    
    // Constructor with parameters
    public Project(String name, String description, String members) {
        this.name = name;
        this.description = description;
        this.members = members;
    }
    
    // Constructor with all fields
    public Project(int id, int projectManagerID, String name, String description, String members) {
        this.id = id;
        this.projectManagerID = projectManagerID;
        this.name = name;
        this.description = description;
        this.members = members;
    }
    
    // Getters and Setters
    public int getId() {
        return id;
    }
    
    public void setId(int id) {
        this.id = id;
    }
    
    public int getProjectManagerID() {
        return projectManagerID;
    }
    
    public void setProjectManagerID(int projectManagerID) {
        this.projectManagerID = projectManagerID;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getMembers() {
        return members;
    }
    
    public void setMembers(String members) {
        this.members = members;
    }
    
    public String getManagerName() {
        return managerName;
    }
    
    public void setManagerName(String managerName) {
        this.managerName = managerName;
    }
    
    @Override
    public String toString() {
        return "Project{" +
                "id=" + id +
                ", projectManagerID=" + projectManagerID +
                ", name='" + name + '\'' +
                ", description='" + description + '\'' +
                ", members='" + members + '\'' +
                '}';
    }
}
