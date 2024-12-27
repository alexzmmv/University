package model.programStateComponents;

import model.adts.MyStack;
import model.statement.IStatement;

import java.util.List;

public class ExecutionStack extends MyStack<IStatement> implements IExecutionStack {
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
    @Override
    public boolean isEmpty() {
        return super.isEmpty();
    }

    @Override
    public List<IStatement> toList() {
        return super.getList();
    }

}
