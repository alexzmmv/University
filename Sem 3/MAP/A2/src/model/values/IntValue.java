package model.values;

import model.type.IType;
import model.type.IntType;

public class IntValue implements IValue {
    int val;

    @Override
    public String toString() {return Integer.toString(val);}

    @Override
    public IType getType() {
        return new IntType();
    }

    public IntValue(int v) {
        val = v;
    }

    public IntValue() {
        val = 0;
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof IntValue) {
            return ((IntValue) other).getVal() == val;
        }
        return false;
    }


    public int getVal() {
        return val;
    }
}
