package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExpressionException;


public interface IStatement {
    ProgramState execute(ProgramState state) throws ExpressionException, AdtException;
    String toString();
}