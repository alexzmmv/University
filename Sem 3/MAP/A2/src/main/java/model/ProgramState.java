package model;

import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.programStateComponents.*;
import model.statement.IStatement;

public class ProgramState {

    ExecutionStack executionStack;
    SymbolTable symbolTable;
    Output output;
    FileTable fileTable;
    IHeap heapTable;
    IStatement originalProgram;
    int id;
    static int nextID = 0;

    public ProgramState(IExecutionStack executionStack,ISymbolTable symTable,IOutput output,IFileTable fileTable,IHeap heap,IStatement statement){
        synchronized (ProgramState.class){
            this.id = nextID++;
        }

        this.executionStack = (ExecutionStack) executionStack;
        this.symbolTable = (SymbolTable) symTable;
        this.output = (Output) output;
        this.fileTable = (FileTable) fileTable;
        this.heapTable = heap;
        this.originalProgram = statement;
        this.executionStack.push(statement);
    }
    public ProgramState(){}

    @Override
    public String toString() {
        return "ProgramState(id= " + id + "){"+
                "executionStack=" + executionStack.toString() +
                "; symbolTable=" + symbolTable.toString() +
                "; output=" + output.toString() +
                "; fileTable=" + fileTable.toString() +
                "; originalProgram=" + originalProgram.toString() +
                '}';
    }

    public boolean isNotCompletedYet(){
        return !executionStack.isEmpty();
    }

    public ProgramState oneStep() throws AdtException, ExpressionException, ExecutionException {
        if(executionStack.isEmpty())
            throw new ExecutionException("Execution stack is empty");
        IStatement currentStatement = executionStack.pop();
        return currentStatement.execute(this);
    }

    public boolean isDefined(String varName) {
        return symbolTable.isDefined(varName);
    }


    public ExecutionStack getExecutionStack() {
        return executionStack;
    }

    public void setExecutionStack(ExecutionStack executionStack) {
        this.executionStack = executionStack;
    }

    public SymbolTable getSymbolTable() {
        return symbolTable;
    }

    public void setSymbolTable(SymbolTable symbolTable) {
        this.symbolTable = symbolTable;
    }

    public Output getOutput() {
        return output;
    }

    public void setOutput(Output output) {
        this.output = output;
    }

    public FileTable getFileTable() {
        return fileTable;
    }

    public void setFileTable(FileTable fileTable) {
        this.fileTable = fileTable;
    }

    public IHeap getHeapTable() {
        return heapTable;
    }

    public void setHeapTable(HeapTable heapTable) {
        this.heapTable = heapTable;
    }

    public IStatement getOriginalProgram() {
        return originalProgram;
    }

    public void setOriginalProgram(IStatement originalProgram) {
        this.originalProgram = originalProgram;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public static int getNextID() {
        return nextID;
    }

    public static void setNextID(int nextID) {
        ProgramState.nextID = nextID;
    }
}
