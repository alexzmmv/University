package repository;

import model.ProgramState;
import model.exception.ExecutionException;

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
    public void logProgramStateExecution() throws ExecutionException, IOException {
        PrintWriter logFile = new PrintWriter(new BufferedWriter(new FileWriter(logFilePath, true)));
        logFile.println("ExeStack:");
        String executionStackString = currentProgram.getExecutionStack().toString();
        executionStackString=executionStackString.replace("|", "\n");
        //executionStackString=executionStackString.replace(",", "\n");
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
        String fileTableString = currentProgram.getFileTable().toString();
        fileTableString=fileTableString.replace("|", "\n");
        logFile.println(fileTableString);
        logFile.println("------------------------------------");
        logFile.close();
    }

    @Override
    public ProgramState getCurrentProgram() {
        return currentProgram;
    }



}
