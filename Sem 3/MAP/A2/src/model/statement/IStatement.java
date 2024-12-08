package model.statement;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;


public interface IStatement {
    ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException;
    String toString();
}