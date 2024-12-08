package model.programStateComponents;

import model.adts.MyDictionary;
import model.adts.MyIDictionary;
import exception.AdtException;
import exception.InvalidAddressException;
import model.values.IValue;

import java.util.Map;

public class HeapTable implements IHeap {
    MyIDictionary<Integer, IValue> heapTable;
    Integer nextFreeAddress;
    public HeapTable() {
        this.heapTable = new MyDictionary<Integer,IValue>();
        this.nextFreeAddress = 1;
    }

    @Override
    public int allocate(IValue value) throws InvalidAddressException {
        try {
            this.heapTable.put(this.nextFreeAddress, value);
            this.nextFreeAddress++;
            return this.nextFreeAddress - 1;
        } catch (AdtException e) {
            throw new InvalidAddressException("Address "+Integer.toString(this.nextFreeAddress)+" not found in heap table or out of bounds");
        }
    }

    @Override
    public void deallocate(int address) throws InvalidAddressException {
        try{
            this.heapTable.remove(address);
        } catch (Exception e) {
            throw new InvalidAddressException("Address "+Integer.toString(address)+" not found in heap table or out of bounds");
        }
    }

    @Override
    public void write(int address, IValue value) throws InvalidAddressException {
        if(!this.heapTable.isDefined(address)) {
            throw new InvalidAddressException("Address "+Integer.toString(address)+" out of bounds");
        }
        try {
            heapTable.give(address, value);
        } catch (AdtException e) {
            throw new InvalidAddressException("Address "+Integer.toString(address)+" not found in heap table or out of bounds");
        }
    }

    @Override
    public IValue read(int address) throws InvalidAddressException {
     try{
            return heapTable.lookup(address);
     } catch (AdtException e) {
         throw new InvalidAddressException("Address "+Integer.toString(address)+" not found in heap table or out of bounds");
     }
    }

    @Override
    public boolean contains(int address) {
        return this.heapTable.isDefined(address);
    }

    @Override
    public Map<Integer, IValue> toMap() {
        return this.heapTable.toMap();
    }

    @Override
    public String toString() {
        return this.heapTable.toString();
    }

}
