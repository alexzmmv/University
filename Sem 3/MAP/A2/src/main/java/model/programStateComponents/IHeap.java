package model.programStateComponents;

import exception.AdtException;
import exception.InvalidAddressException;
import model.values.IValue;

import java.util.Map;

public interface IHeap {
    int allocate(IValue value) throws AdtException;

    void deallocate(int address) throws InvalidAddressException;

    void write(int address, IValue value) throws InvalidAddressException;

    IValue read(int address) throws InvalidAddressException;

    boolean contains(int address);

    Map<Integer, IValue> toMap();

}
