package model.type;

import model.values.IValue;

public interface IType {
    String toString();

    IValue defaultValue();
}
