package model.type;

import model.values.IValue;
import model.values.ReferenceValue;

public class ReferenceType implements IType{

    public void setInner(IType inner) {
        this.inner = inner;
    }

    IType inner;
    public ReferenceType(IType inner) {this.inner=inner;}
    public ReferenceType() {};
    public IType getInner() {return inner;}

    public boolean equals(Object another) {
        if (another instanceof ReferenceType)
            return inner.equals(((ReferenceType) another).getInner());
        return false;
    }
    public String toString() { return "Ref(" +inner.toString()+")";}

    @Override
    public IValue defaultValue() { return new ReferenceValue(0,inner);}


}
