package utils;

import java.util.HashMap;

public class MyDictionary<K,V> implements MyIDictionary<K,V> {
    HashMap<K,V> dict;
    public MyDictionary(){
        dict = new HashMap<K,V>();
    }
    public void put(K key, V value){
        dict.put(key, value);
    }
    public V get(K key){
        return dict.get(key);
    }
    public boolean contains(K key){
        return dict.containsKey(key);
    }
    public void remove(K key){
        dict.remove(key);
    }
}
