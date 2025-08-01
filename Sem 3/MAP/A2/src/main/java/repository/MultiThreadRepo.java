package repository;

import model.ProgramState;
import exception.AdtException;
import exception.LogFileException;
import model.programStateComponents.FileTable;
import model.programStateComponents.HeapTable;
import model.programStateComponents.IHeap;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

public class MultiThreadRepo implements IRepo {

    private String logFilePath;
    private List<ProgramState> programStates;

    public MultiThreadRepo(ProgramState currentProgram, String logFilePath) {
        programStates = new ArrayList<>();
        programStates.add(currentProgram);
        this.logFilePath = logFilePath;
    }

    public MultiThreadRepo() {
        programStates = new ArrayList<>();
        this.logFilePath = "xlog.txt";

    }

    public void setLogFilePath(String logFilePath) {
        this.logFilePath = logFilePath;
    }
    @Override
    public String getLogFilePath() {
        return logFilePath;
    }


    @Override
    public void logProgramStateExecution(ProgramState currentProgram) throws LogFileException {
        PrintWriter logFile;
        try {
            logFile = new PrintWriter(new BufferedWriter(new FileWriter(logFilePath, true)));
        }
        catch(IOException e){
            throw new LogFileException("Could not open file:"+e.getMessage());
        }

        logFile.println("Program ID: " + currentProgram.getId());
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

        logFile.println("Heap:");
        IHeap heap = currentProgram.getHeapTable();
        outString = heap.toString();
        outString=outString.replace("|", "\n");
        logFile.println(outString);
        logFile.println("--------------------------------------");
        logFile.close();
    }

    @Override
    public List<ProgramState> getProgramList() {
        return programStates;
    }

    @Override
    public void setProgramList(List<ProgramState> programList) {
        this.programStates = programList;
    }

    @Override
    public void addProgram(ProgramState e) {
        programStates.add(e);
    }

    @Override
    public void clear() {
        programStates.clear();
    }


}
