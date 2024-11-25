package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.expresion.IExpression;
import model.values.IValue;
import model.values.ReferenceValue;

public class newStatement implements IStatement{
    String name;
    IExpression expression;

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        state.getSymbolTable().give(name,new ReferenceValue(state.getHeapTable().allocate(value), value.getType()));
        return state;
    }

    @Override
    public String toString() {
        return "new(" + name + "," + expression.toString() + ")";
    }
}
