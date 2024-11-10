package repository;

import model.Atendee;

public interface RepositoryInterface {
    Atendee[] getAttendee(String name);

    Integer getSize();

    void addAtendee(Atendee atendee) throws Exception;

    void deleteAtendee(String name) throws Exception;

    Atendee[] getAtendees();

    Boolean isAtendee(String name);
}
