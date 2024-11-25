package repository;

import model.ProgramState;
import model.adts.MyTree;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.LogFileException;
import model.programStateComponents.FileTable;
import model.statement.IStatement;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class SingleThreadRepo implements IRepo {

    private ProgramState currentProgram;
    private String logFilePath;


    public SingleThreadRepo(ProgramState currentProgram, String logFilePath) {
        this.currentProgram = currentProgram;
        this.logFilePath = logFilePath;
    }

    public void setCurrentProgram(ProgramState currentProgram) {
        this.currentProgram = currentProgram;
    }


    public void setLogFilePath(String logFilePath) {
        this.logFilePath = logFilePath;
    }

    public String getLogFilePath() {
        return logFilePath;
    }

    @Override
    public void logProgramStateExecution() throws LogFileException, AdtException {
        PrintWriter logFile;
        try {
            logFile = new PrintWriter(new BufferedWriter(new FileWriter(logFilePath, true)));
        }
        catch(IOException e){
            throw new LogFileException("Could not open file:"+e.getMessage());
        }


        logFile.println("Execution Stack:");
        String executionStackString = currentProgram.getExecutionStack().toString();
        executionStackString=executionStackString.replace("|", "\n");

        logFile.println(executionStackString);
        logFile.println("SymTable:");
        String symbolTableString = currentProgram.getSymbolTable().toString();
        symbolTableString=symbolTableString.replace("|", "\n");
        logFile.println(symbolTableString);
        logFile.println("Out:");
        String outString = currentProgram.getOutput().toString();
        outString=outString.replace("|", "\n");
        logFile.println(outString);
        logFile.println("FileTable:");
        FileTable fileTable = (FileTable) currentProgram.getFileTable();
        String fileTableString = fileTable.toString();
        logFile.println(fileTableString);
        /*
        logFile.println("Heap:");
        Heap heap = (Heap) currentProgram.getHeap();
        String heapString = heap.toString();
        logFile.println(heapString);
         */
        logFile.println("--------------------------------------");
        logFile.close();
    }

    @Override
    public ProgramState getCurrentProgram() {
        return currentProgram;
    }



}
