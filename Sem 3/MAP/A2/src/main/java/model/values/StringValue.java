package model.values;

import model.type.IType;
import model.type.StringType;

public class StringValue implements IValue {

    String val;

    public StringValue(String v) {
        val = v;
    }

    public StringValue() {
        val = "";
    }

    public String getVal() {
        return val;
    }

    @Override
    public IType getType() {
        return new StringType();
    }

    @Override
    public String toString() {
        return "\""+val+"\"";
    }

    @Override
    public boolean equals(Object other) {
        if (other instanceof StringValue) {
            return ((StringValue) other).getVal().equals(val);
        }
        return false;
    }
}
