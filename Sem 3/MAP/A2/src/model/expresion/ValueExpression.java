package model.expresion;

import exception.AdtException;
import exception.TypeNotMatchException;
import model.ProgramState;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.type.IType;
import model.values.IValue;

public class ValueExpression implements IExpression {

    IValue value;


    public ValueExpression(IValue val) {
        this.value = val;
    }

    @Override
    public IValue evaluate(ProgramState state) throws ExpressionException {
        return value;
    }

    @Override
    public String toString() {
        return value.toString();
    }

    @Override
    public IType typeCheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException, AdtException {
        return value.getType();
    }
}
