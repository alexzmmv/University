package repository;

import model.Atendee;

public class InMemoryRepository implements RepositoryInterface {
    private Atendee[] atendees=new Atendee[100];
    private Integer size,capacity;
    public InMemoryRepository(){
        size=0;
        capacity=100;
    }
    @Override
    public Atendee[] getAttendee(String name) {
        return atendees;
    }

    @Override
    public Integer getSize() {
        return size;
    }

    @Override
    public void addAtendee(Atendee atendee) throws Exception {
        if(size==capacity)
            throw new Exception("No more space");
        if(isAtendee(atendee.getName()))
            throw new Exception("Atendee already exists");
        atendees[size]=atendee;
        size++;
    }

    @Override
    public void deleteAtendee(String name) throws Exception {
        for(int i=0;i<size;i++){
            if(atendees[i].getName().equals(name)){
                for(int j=i;j<size-1;j++){
                    atendees[j]=atendees[j+1];
                }
                size--;
                return;
            }
        }
        throw new Exception("Atendee not found");
    }

    @Override
    public Atendee[] getAtendees() {
        return atendees;
    }

    @Override
    public Boolean isAtendee(String name) {
        for(int i=0;i<size;i++){
            if(atendees[i].getName().equals(name))
                return true;
        }
        return false;
    }

}
