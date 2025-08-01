package model.adts;

import exception.AdtException;
import model.values.IValue;

import java.util.*;

public class MyDictionary<K,V> implements MyIDictionary<K,V> {
    protected HashMap<K,V> dict;
    public MyDictionary(){
        dict = new HashMap<K,V>();
    }

    protected List<V> getValues() {
        return (List<V>) dict.values();
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

    public V lookup(K key) throws AdtException {
        if(!dict.containsKey(key))
            throw new AdtException("Key not found in dictionary");
        return dict.get(key);
    }

    @Override
    public boolean isDefined(K id) {
        return dict.containsKey(id);
    }

    public void remove(K key){
        dict.remove(key);
    }

    @Override
    public String toString() {
        String outS = "";
        for (K key : dict.keySet()) {
            outS = outS + key.toString() + " --> " + dict.get(key).toString() + "|";
        }
        return outS;
    }

    @Override
    public Map<K, V> toMap() {
        return this.dict;
    }

    public MyDictionary<K,V> copy() {
        MyDictionary<K,V> newDict = new MyDictionary<>();
        for (K key : dict.keySet()) {
            newDict.dict.put(key, dict.get(key));
        }
        return newDict;
    }

    protected List<IValue> getKeys() {
        return new ArrayList<IValue>((Collection<? extends IValue>) dict.keySet());
    }
}
