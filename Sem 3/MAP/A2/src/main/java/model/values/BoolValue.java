package model.values;

import model.type.BoolType;
import model.type.IType;

public class BoolValue implements IValue {
    boolean val;

    public BoolValue(boolean v) {
        val = v;
    }

    public BoolValue() {
        val = false;
    }
    public boolean getVal() {
        return val;
    }

    @Override
    public String toString() {
        return val? "True" : "False";
    }

    @Override
    public IType getType() {
        return new BoolType();
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof BoolValue) {
            return ((BoolValue) other).getVal() == val;
        }
        return false;
    }


}
