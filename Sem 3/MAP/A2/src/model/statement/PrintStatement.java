package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.expresion.IExpression;

public class PrintStatement implements IStatement{
    IExpression expression;

    public PrintStatement(IExpression expression) {
        this.expression = expression;
    }

    @Override
    public String toString() {
        return "print["+expression.toString()+"]";
    }
    @Override
    public ProgramState execute(ProgramState state) throws AdtException, ExpressionException, ExecutionException {
        state.getOutput().add(expression.evaluate(state));
        return state;
    }
}
