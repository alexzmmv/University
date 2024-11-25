package model.expresion;

import model.ProgramState;
import model.exception.ExpressionException;
import model.programStateComponents.SymbolTable;
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
}
