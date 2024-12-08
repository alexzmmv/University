package model.statement;

import model.ProgramState;
import exception.AdtException;
import exception.ExpressionException;

public class NopStatement implements IStatement {

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException {
        return null;
    }

    public String toString() {
        return "nop";
    }
}
