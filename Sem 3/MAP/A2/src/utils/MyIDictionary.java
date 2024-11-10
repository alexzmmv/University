package utils;

public interface MyIDictionary<K,V> {
    void put(K key, V value);
    V get(K key);
    boolean contains(K key);
}
