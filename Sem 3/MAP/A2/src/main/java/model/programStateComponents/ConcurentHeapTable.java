package model.programStateComponents;

import exception.AdtException;
import exception.InvalidAddressException;
import model.adts.ConcurentMyDictionary;
import model.adts.MyDictionary;
import model.adts.MyIDictionary;
import model.values.IValue;

import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurentHeapTable implements IHeap{
    private AtomicInteger nextFreeAddress;
    private MyIDictionary<Integer, IValue> heapTable;

    public ConcurentHeapTable() {
        nextFreeAddress = new AtomicInteger(1);
        heapTable = new ConcurentMyDictionary<Integer, IValue>();
    }
    @Override
    public int allocate(IValue value) throws InvalidAddressException {
        try {
            this.heapTable.put(this.nextFreeAddress.get(), value);
            this.nextFreeAddress.incrementAndGet();
            return this.nextFreeAddress.get() - 1;
        } catch (AdtException e) {
            throw new InvalidAddressException("Address "+Integer.toString(this.nextFreeAddress.get())+" not found in heap table or out of bounds");
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
