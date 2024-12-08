package model.adts;

import exception.AdtException;

public interface MyIList<T> {
    void add(T el);
    T get(int index) throws AdtException;
    int size();
    boolean contains(T el);

    String toString();
}
