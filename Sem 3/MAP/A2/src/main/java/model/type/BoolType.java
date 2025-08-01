package model.type;

import model.values.BoolValue;
import model.values.IValue;

public class BoolType implements IType {
    public BoolType() {}

    public String toString() {
        return "Bool";
    }

    @Override
    public IValue defaultValue() {
        return new BoolValue(false);
    }

    public boolean equals(Object obj) {
        return obj instanceof BoolType;
    }
}
