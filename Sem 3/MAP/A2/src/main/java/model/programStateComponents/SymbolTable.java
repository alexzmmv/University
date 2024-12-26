package model.programStateComponents;

import model.adts.MyDictionary;
import exception.AdtException;
import model.values.IValue;

import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class SymbolTable extends MyDictionary<String, IValue> implements ISymbolTable {
    @Override
    public void put(String key, IValue value) throws AdtException {
        super.put(key, value);
    }

    @Override
    public void give(String key, IValue value) throws AdtException {
        super.give(key, value);
    }

    @Override
    public IValue lookup(String key) throws AdtException {
        return super.lookup(key);
    }

    @Override
    public boolean isDefined(String id) {
        return super.isDefined(id);
    }

    @Override
    public void remove(String key) {
        super.remove(key);
    }

    public SymbolTable() {
        super();
    }

    public SymbolTable(MyDictionary<String, IValue> table) {
        super();
    }


    public String toString() {
        return super.toString();
    }


    public SymbolTable copy() {
        SymbolTable newTable = new SymbolTable();
        for (String key : super.dict.keySet()){
            newTable.dict.put(key, super.dict.get(key));
        }
        return newTable;
    }

    public Map<String, IValue> toMap(){
        return super.toMap();
    }
}
