package model.adts;

import model.exception.AdtException;

public interface MyIDictionary<K,V> {
    void put(K key, V value) throws AdtException;
    void give(K key, V value) throws AdtException;
    V lookup(K key) throws AdtException;
    boolean isDefined(K id);
    void remove(K stringValue);
}
