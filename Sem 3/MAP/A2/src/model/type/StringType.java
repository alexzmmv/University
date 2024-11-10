package model.type;

import model.values.IValue;
import model.values.StringValue;

public class StringType implements IType {
    @Override
    public IValue defaultValue() {
        return new StringValue("");
    }

    public String toString() {
        return "String";
    }

    public boolean equals(Object obj) {
        return obj instanceof StringType;
    }
}
