package model.adts;

import exception.AdtException;

public interface MyIStack <T>{
    T pop() throws AdtException;
    void push(T el);
    T top();
    String toString();
    boolean isEmpty();

    T peek();
}
