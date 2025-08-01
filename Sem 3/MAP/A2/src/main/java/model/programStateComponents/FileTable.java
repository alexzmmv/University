package model.programStateComponents;

import model.adts.MyDictionary;
import exception.AdtException;
import model.values.IValue;
import model.values.StringValue;

import java.io.BufferedReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class FileTable extends MyDictionary<StringValue, BufferedReader> implements IFileTable {
    public FileTable() {
        super();
    }

    public FileTable(MyDictionary<StringValue, BufferedReader> table) {
        super();
    }

    @Override
    public void put(StringValue key, BufferedReader value) throws AdtException {
        super.put(key, value);
    }

    @Override
    public void give(StringValue key, BufferedReader value) throws AdtException {
        super.give(key, value);
    }

    @Override
    public BufferedReader lookup(StringValue key) throws AdtException {
        return super.lookup(key);
    }

    @Override
    public boolean isDefined(StringValue id) {
        return super.isDefined(id);
    }

    @Override
    public void remove(StringValue key) {
        super.remove(key);
    }

    public String toString() {
        String result = "";
        for(StringValue key : dict.keySet()) {
            result =result+key.toString() +"\n";
        }
        return result;
    }

    @Override
    public List<IValue> getFileList() {
        return new ArrayList<>(super.getKeys());
    }

}
