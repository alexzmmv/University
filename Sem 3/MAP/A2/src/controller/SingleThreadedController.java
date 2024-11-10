package controller;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import model.exception.FileException;
import repository.IRepo;

import java.io.IOException;

public class SingleThreadedController implements IController{
    IRepo repo;

    public SingleThreadedController(IRepo repo){
        this.repo = repo;
    }
    @Override
    public void executeOneStep() throws AdtException, ExpressionException, ExecutionException, FileException {
        ProgramState programState = repo.getCurrentProgram();
        programState.oneStep();
    }

    @Override
    public void executeAll() throws AdtException, ExpressionException, ExecutionException, IOException {
        ProgramState programState = repo.getCurrentProgram();
        while (!programState.getExecutionStack().isEmpty()){
            programState.oneStep();
            repo.logProgramStateExecution();
        }
    }

    public IRepo getRepo() {
        return repo;
    }

    public void setRepo(IRepo repo) {
        this.repo = repo;
    }
}
