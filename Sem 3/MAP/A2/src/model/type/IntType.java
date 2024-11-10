package model.type;

import model.values.IValue;
import model.values.IntValue;

public class IntType implements IType {
    public IntType() {}

    public String toString() {
        return "Integer";
    }

    @Override
    public IValue defaultValue() {
        return new IntValue(0);
    }

    public boolean equals(Object obj) {
        return obj instanceof IntType;
    }

}
