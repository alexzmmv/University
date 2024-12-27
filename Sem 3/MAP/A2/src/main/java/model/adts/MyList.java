package model.adts;


import exception.AdtException;
import model.values.IValue;

import java.util.LinkedList;
import java.util.List;

public class MyList <T> implements MyIList<T> {
    List<T> list;
    public MyList() {
        list = new LinkedList<T>();
    }

    @Override
    public void add(T el) {
        list.add(el);
    }

    @Override
    public T get(int index) throws AdtException {
        if(index < 0 || index >= list.size())
            throw new AdtException("Index out of bounds");
        return list.get(index);
    }

    @Override
    public int size() {
        return list.size();
    }

    @Override
    public boolean contains(T el) {
        return list.contains(el);
    }

    @Override
    public String toString() {
        String outStr = "";
        for (T el : list) {
            outStr = outStr + el.toString() + "|";
        }
        return outStr;
    }

    protected List<T> getList() {
        return (List<T>) list;
    }
}
