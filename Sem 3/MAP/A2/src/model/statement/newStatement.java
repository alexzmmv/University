package model.statement;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.expresion.IExpression;
import model.expresion.ValueExpression;
import model.values.IValue;
import model.values.IntValue;
import model.values.ReferenceValue;

public class newStatement implements IStatement{
    String name;
    IExpression expression;

    public newStatement(String name) {
        this.name = name;
        expression = new ValueExpression(new IntValue());
    }

    public newStatement(String name, IExpression expression) {
        this.name = name;
        this.expression = expression;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        state.getSymbolTable().give(name,new ReferenceValue(state.getHeapTable().allocate(value), value.getType()));
        return null;
    }

    @Override
    public String toString() {
        return "new(" + name + "," + expression.toString() + ")";
    }
}
