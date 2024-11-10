package model;

import model.adts.MyIDictionary;
import model.adts.MyIList;
import model.adts.MyIStack;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.programStateComponents.SymbolTable;
import model.statement.IStatement;
import model.values.IValue;
import model.values.StringValue;

import java.io.BufferedReader;

public class ProgramState {
    public ProgramState(MyIStack<IStatement> executionStack, MyIDictionary<String, IValue> symbolTable, MyIList<IValue> output, MyIDictionary<StringValue, BufferedReader> fileTable, IStatement originalProgram) {
        this.executionStack = executionStack;
        this.symbolTable = symbolTable;
        this.output = output;
        this.fileTable = fileTable;
        this.originalProgram = originalProgram;
        executionStack.push(originalProgram);
    }

    public MyIStack<IStatement> getExecutionStack() {
        return executionStack;
    }

    public void setExecutionStack(MyIStack<IStatement> executionStack) {
        this.executionStack = executionStack;
    }

    public SymbolTable getSymbolTable() {
        return (SymbolTable) symbolTable;
    }

    public void setSymbolTable(MyIDictionary<String, IValue> symbolTable) {
        this.symbolTable = symbolTable;
    }

    public MyIList<IValue> getOutput() {
        return output;
    }

    public void setOutput(MyIList<IValue> output) {
        this.output = output;
    }

    public MyIDictionary<StringValue, BufferedReader> getFileTable() {
        return fileTable;
    }

    public void setFileTable(MyIDictionary<StringValue, BufferedReader> fileTable) {
        this.fileTable = fileTable;
    }

    MyIStack<IStatement> executionStack;
    MyIDictionary<String, IValue> symbolTable;
    MyIList<IValue> output;
    MyIDictionary<StringValue, BufferedReader> fileTable;
    IStatement originalProgram;


    public ProgramState(){}

    @Override
    public String toString() {
        return "ProgramState{" +
                "executionStack=" + executionStack.toString() +
                "; symbolTable=" + symbolTable.toString() +
                "; output=" + output.toString() +
                "; fileTable=" + fileTable.toString() +
                "; originalProgram=" + originalProgram.toString() +
                '}';
    }

    public IStatement getOriginalProgram() {
        return originalProgram;
    }

    public void setOriginalProgram(IStatement originalProgram) {
        this.originalProgram = originalProgram;
    }

    public ProgramState oneStep() throws ExecutionException, AdtException, ExpressionException {
        if (executionStack.isEmpty()) {
            throw new ExecutionException("Execution stack is empty");
        }
        IStatement currentStatement = executionStack.pop();
        return currentStatement.execute(this);
    }
}
