package model.statement;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.programStateComponents.ExecutionStack;

public class ForkStatement implements IStatement{
    IStatement innerStatement;

    public ForkStatement(IStatement innerStatement) {
        this.innerStatement = innerStatement;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        return new ProgramState(new ExecutionStack(),state.getSymbolTable().copy(),state.getOutput(),state.getFileTable(), state.getHeapTable(), innerStatement);
    }

    @Override
    public String toString() {
        return "fork(" + innerStatement.toString() + ")";
    }
}
