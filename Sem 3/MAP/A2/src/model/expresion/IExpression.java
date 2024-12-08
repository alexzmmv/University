package model.expresion;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.values.IValue;

public interface IExpression {
    IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException;
    String toString();
}
