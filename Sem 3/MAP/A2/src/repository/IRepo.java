package repository;

import model.ProgramState;
import model.exception.ExecutionException;

import java.io.IOException;

public interface IRepo {
    void logProgramStateExecution() throws ExecutionException, IOException;
    ProgramState getCurrentProgram();
    void setCurrentProgram(ProgramState currentProgram);
}
