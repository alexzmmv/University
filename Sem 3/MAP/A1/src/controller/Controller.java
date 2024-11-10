package controller;
import model.*;
import repository.*;

@SuppressWarnings("ReassignedVariable")
public class Controller {
    RepositoryInterface repository;
    public Controller(RepositoryInterface repository){
        this.repository = repository;
    }

    public void addAttendee(String name, Boolean present, String type) throws Exception {
        switch (type){
            case "professor":
                Atendee professor = new Professor(name, present);
                repository.addAtendee(professor);
                break;
            case "student":
                Atendee student = new Student(name, present);
                repository.addAtendee(student);
                break;
            case "expert":
                Atendee expert = new Expert(name, present);
                repository.addAtendee(expert);
                break;
            default:
                throw new Exception("Invalid type");
        }
    }
    public void deleteAttendee(String name) throws Exception {
        repository.deleteAtendee(name);
    }

    public Pair<Atendee[],Integer> getPresentingAtendees(){
        Atendee[] atendees = repository.getAtendees();
        Atendee[] presentators = new Atendee[100];
        Integer size = repository.getSize();
        Integer presentatorsSize = 0;
        for(int i=0;i<size;i++){
            if(atendees[i].isPresenting()){
                presentators[presentatorsSize] = atendees[i];
                presentatorsSize++;
            }
        }
        return new Pair<>(presentators,presentatorsSize);
    }
    public Pair<Atendee[],Integer> getAtendees(){
        Atendee[] atendees = repository.getAtendees();
        Integer size = repository.getSize();
        return new Pair<>(atendees,size);
    }

}
