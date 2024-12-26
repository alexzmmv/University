package repository;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;

import java.io.IOException;
import java.util.List;

public interface IRepo {
    void logProgramStateExecution(ProgramState prg) throws ExecutionException, IOException, AdtException;
    List<ProgramState> getProgramList();
    void setProgramList(List<ProgramState> programList);
    public String getLogFilePath();

    void addProgram(ProgramState e);

    void clear();

}
