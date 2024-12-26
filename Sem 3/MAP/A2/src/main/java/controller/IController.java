package controller;

import exception.InterpreterException;
import model.ProgramState;
import model.statement.IStatement;

import java.util.List;

public interface IController {
    public void executeOneStep() throws InterpreterException;
    public void displayCurrentState() throws InterpreterException;
    public void removeCompletedPrograms();
    void executeAllSteps() throws InterpreterException;

    public void setDisplayFlag(boolean displayFlag);
    void setProgram(IStatement statement) throws InterpreterException;
    void setProgramList(List<ProgramState> programList);
    public List<ProgramState> getProgramList();

}