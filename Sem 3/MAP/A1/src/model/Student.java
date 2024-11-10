package model;

public class Student implements Atendee {
    Boolean presents;
    String name;
    public Student(String name, Boolean present){
        this.presents=present;
        this.name=name;
    }

    @Override
    public void setPresents(Boolean prs) {
        presents=prs;
    }

    @Override
    public Boolean isPresenting() {
        return this.presents;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String toString(){
        return "Student: " + this.name + " " + (this.presents ? "presentator" : "");
    }


}
