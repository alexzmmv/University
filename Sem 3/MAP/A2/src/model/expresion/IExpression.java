package model.expresion;

import model.exception.AdtException;
import model.exception.ExpressionException;
import model.programStateComponents.SymbolTable;
import model.values.IValue;

public interface IExpression {
    IValue evaluate(SymbolTable table) throws ExpressionException, AdtException;
    String toString();
}
