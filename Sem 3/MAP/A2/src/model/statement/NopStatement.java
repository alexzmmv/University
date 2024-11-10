package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExpressionException;

public class NopStatement implements IStatement {

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException {
        return state;
    }

    public String toString() {
        return "nop";
    }
}
