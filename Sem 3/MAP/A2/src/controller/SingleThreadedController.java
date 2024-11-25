package controller;

import model.ProgramState;
import model.exception.*;
import repository.IRepo;

import java.io.IOException;
import java.io.PrintWriter;

public class SingleThreadedController implements IController{
    IRepo repo;

    public SingleThreadedController(IRepo repo){
        this.repo = repo;
    }
    @Override
    public void executeOneStep() throws AdtException, ExpressionException, ExecutionException, FileException, LogFileException {
        ProgramState programState = repo.getCurrentProgram();
        programState.oneStep();

        try {
            repo.logProgramStateExecution();
        } catch (IOException e) {
            throw new LogFileException("Could not log program state execution:"+e.getMessage());
        }
    }

    @Override
    public void executeAll(Boolean flag) throws AdtException, ExpressionException, ExecutionException {
        ProgramState programState = repo.getCurrentProgram();
        while (!programState.getExecutionStack().isEmpty()){
            programState.oneStep();
            try {
                repo.logProgramStateExecution();
            } catch (IOException e) {
                throw new LogFileException("Could not log program state execution:"+e.getMessage());
            }

            if(flag)
                System.out.println(programState);
        }
    }

    public IRepo getRepo() {
        return repo;
    }

    public void setRepo(IRepo repo) {
        this.repo = repo;
    }
}
