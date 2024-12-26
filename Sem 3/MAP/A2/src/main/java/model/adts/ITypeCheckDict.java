package model.adts;

import exception.AdtException;

public interface ITypeCheckDict<K, V>{
    V lookup(K key) throws AdtException;
    void put(K key, V value) throws AdtException;
    void give(K key, V value) throws AdtException;
    void remove(K key);
    boolean isDefined(K key);
    ITypeCheckDict<K, V> copy();
    String toString();
}
