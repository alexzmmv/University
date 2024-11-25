package model.programStateComponents;

import model.adts.MyStack;
import model.exception.AdtException;
import model.statement.IStatement;
import model.values.StringValue;

import java.io.BufferedReader;

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
}
