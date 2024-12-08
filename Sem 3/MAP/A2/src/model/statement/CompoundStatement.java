package model.statement;

import model.ProgramState;
import model.adts.MyIStack;
import exception.AdtException;
import exception.ExpressionException;

public class CompoundStatement implements IStatement {
    IStatement first;
    IStatement second;

    public CompoundStatement(IStatement first, IStatement second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public ProgramState execute(ProgramState state) throws AdtException, ExpressionException {
        MyIStack<IStatement> stack = state.getExecutionStack();
        stack.push(second);
        stack.push(first);
        return null;
    }

    @Override
    public String toString() {
        return first.toString() + " , " + second.toString();
    }
}
