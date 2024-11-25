package model.expresion;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.programStateComponents.SymbolTable;
import model.values.IValue;

public interface IExpression {
    IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException;
    String toString();
}
