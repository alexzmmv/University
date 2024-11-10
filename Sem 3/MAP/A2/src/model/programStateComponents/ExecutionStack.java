package model.programStateComponents;

import model.adts.MyStack;
import model.statement.IStatement;

public class ExecutionStack extends MyStack<IStatement> {
    public ExecutionStack() {
        super();
    }

    public ExecutionStack(IStatement statement) {
        super();
    }

    public ExecutionStack(MyStack<IStatement> stack) {
        super();
    }

    public String toString() {
        return super.toString();
    }
}
