package model;

import model.adts.MyIDictionary;
import model.adts.MyIList;
import model.adts.MyIStack;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.programStateComponents.*;
import model.statement.IStatement;
import model.values.IValue;
import model.values.StringValue;

import java.io.BufferedReader;

public class ProgramState {

    public HeapTable getHeapTable() {
        return heapTable;
    }

    public void setHeapTable(HeapTable heapTable) {
        this.heapTable = heapTable;
    }

    public void setFileTable(FileTable fileTable) {
        this.fileTable = fileTable;
    }

    public void setOutput(Output output) {
        this.output = output;
    }

    public void setSymbolTable(SymbolTable symbolTable) {
        this.symbolTable = symbolTable;
    }

    public void setExecutionStack(ExecutionStack executionStack) {
        this.executionStack = executionStack;
    }

    public ProgramState(MyIStack<IStatement> executionStack, MyIDictionary<String, IValue> symbolTable, MyIList<IValue> output, MyIDictionary<StringValue, BufferedReader> fileTable, IStatement originalProgram, HeapTable heapTable) {
        this.executionStack = (ExecutionStack) executionStack;
        this.symbolTable = (SymbolTable) symbolTable;
        this.output = (Output) output;
        this.fileTable = (FileTable) fileTable;
        this.heapTable = heapTable;
        this.originalProgram = originalProgram;

        executionStack.push(originalProgram);
    }

    public MyIStack<IStatement> getExecutionStack() {
        return executionStack;
    }

    public void setExecutionStack(MyIStack<IStatement> executionStack) {
        this.executionStack = (ExecutionStack) executionStack;
    }

    public SymbolTable getSymbolTable() {
        return (SymbolTable) symbolTable;
    }

    public void setSymbolTable(MyIDictionary<String, IValue> symbolTable) {
        this.symbolTable = (SymbolTable) symbolTable;
    }

    public MyIList<IValue> getOutput() {
        return output;
    }

    public void setOutput(MyIList<IValue> output) {
        this.output = (Output) output;
    }

    public MyIDictionary<StringValue, BufferedReader> getFileTable() {
        return fileTable;
    }

    public ProgramState(ExecutionStack executionStack, SymbolTable symbolTable, Output output, FileTable fileTable, HeapTable heapTable, IStatement originalProgram) {
        this.executionStack = executionStack;
        this.symbolTable = symbolTable;
        this.output = output;
        this.fileTable = fileTable;
        this.heapTable = heapTable;
        this.originalProgram = originalProgram;
    }

    public void setFileTable(MyIDictionary<StringValue, BufferedReader> fileTable) {
        this.fileTable = (FileTable) fileTable;
    }

    ExecutionStack executionStack;
    SymbolTable symbolTable;
    Output output;
    FileTable fileTable;
    HeapTable heapTable;
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

    public boolean isDefined(String varName) {
        return symbolTable.isDefined(varName);
    }
}
