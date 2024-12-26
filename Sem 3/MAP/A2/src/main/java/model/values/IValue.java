package model.values;

import model.type.IType;

public interface IValue {
    IType getType();
    String toString();
    boolean equals(Object other);
}
