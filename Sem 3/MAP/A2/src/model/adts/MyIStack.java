package model.adts;

import model.exception.AdtException;

public interface MyIStack <T>{
    T pop() throws AdtException;
    void push(T el);
    T top();
    String toString();
    boolean isEmpty();
}
