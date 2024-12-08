package model.adts;

import exception.AdtException;
import model.values.IValue;

import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public interface MyIDictionary<K,V> {
    void put(K key, V value) throws AdtException;
    void give(K key, V value) throws AdtException;
    V lookup(K key) throws AdtException;
    boolean isDefined(K id);
    void remove(K stringValue);

    Map<K, V> toMap();
}
