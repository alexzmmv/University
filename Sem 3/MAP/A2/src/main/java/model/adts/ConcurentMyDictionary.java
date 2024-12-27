package model.adts;

import exception.AdtException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class ConcurentMyDictionary<K,V> implements MyIDictionary<K,V>{
    protected ConcurrentHashMap<K,V> dict;
    public ConcurentMyDictionary(){
        dict = new ConcurrentHashMap<K,V>();
    }

    @Override
    public void put(K key, V value) throws AdtException {
        if(dict.containsKey(key))
            throw new AdtException("Key already exists in dictionary");
        dict.put(key, value);
    }

    @Override
    public void give(K key, V value) throws AdtException {
        if(dict.containsKey(key))
            dict.put(key, value);
        else
            throw new AdtException("Key not found in dictionary");
    }

    @Override
    public V lookup(K key) throws AdtException {
        if(!dict.containsKey(key))
            throw new AdtException("Key not found in dictionary");
        return dict.get(key);
    }

    @Override
    public boolean isDefined(K id) {
        return dict.containsKey(id);
    }

    @Override
    public void remove(K stringValue) {
        dict.remove(stringValue);
    }

    @Override
    public Map<K, V> toMap() {
        return this.dict;
    }

    @Override
    public String toString() {
        String outS = "";
        for (K key : dict.keySet()) {
            outS = outS + key.toString() + " --> " + dict.get(key).toString() + "|";
        }
        return outS;
    }

    public List<K> getKeys() {
        return new ArrayList<>(dict.keySet());
    }
}
