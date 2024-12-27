package controller;

import exception.AdtException;
import exception.ExecutionException;
import exception.InterpreterException;
import model.ProgramState;
import model.programStateComponents.*;
import model.statement.IStatement;
import model.statement.NopStatement;
import repository.IRepo;

import java.io.IOException;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

public class MultiThreadedController implements IController{
    IRepo repo;
    boolean displayFlag;

    ExecutorService executor;

    public MultiThreadedController(IRepo repo, ExecutorService executor, boolean displayFlag){
        this.repo = repo;
        this.executor = executor;
        this.displayFlag = displayFlag;
    }

    public MultiThreadedController(IRepo repo){
        this.repo = repo;
        this.executor = Executors.newSingleThreadExecutor();
        this.displayFlag = true;
    }


    public ExecutorService getExecutor() {
        return executor;
    }

    public void setExecutor(ExecutorService executor) {
        this.executor = executor;
    }

    public boolean isDisplayFlag() {
        return displayFlag;
    }

    @Override
    public void removeCompletedPrograms(){
        this.repo.setProgramList(
                this.repo.getProgramList().stream()
                        .filter(ProgramState::isNotCompletedYet)
                        .collect(Collectors.toList()));
    }
    public void executeOneStep() throws InterpreterException {
        this.removeCompletedPrograms();
        List<Callable<ProgramState>> stepList = repo.getProgramList().stream()
                .map(program -> (Callable<ProgramState>) (() -> {
                    return program.oneStep();
                }))
                .toList();
        List<ProgramState> newPrograms = null;
        try {
            newPrograms = executor.invokeAll(stepList).stream()
                    .map(future -> {
                        try {
                            return future.get();
                        } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                        } catch (java.util.concurrent.ExecutionException e) {
                            try {
                                this.setProgram(new NopStatement());
                                //log on log file the error
                                throw new RuntimeException("Program execution stopped, error:"+e.getMessage());
                            } catch (InterpreterException ex) {
                                throw new RuntimeException(ex);
                            }
                        }
                    })
                    .filter(Objects::nonNull)
                    .toList();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        newPrograms.forEach(e -> this.repo.addProgram(e));
        //garbage collector
        GarbageCollector.runGarbageCollector(this.repo.getProgramList());
        if (displayFlag)
            this.repo.getProgramList().forEach(System.out::println);
        this.repo.getProgramList().forEach(e -> {
            try {
                this.repo.logProgramStateExecution(e);
            } catch (Exception ex) {
                throw new InterpreterException(ex.getMessage());
            }
        });
    }

    @Override
    public void executeAllSteps() throws InterpreterException{
        while(true){
            this.removeCompletedPrograms();
            if(this.repo.getProgramList().isEmpty()){
                break;
            }
            this.executeOneStep();
        }
    }

    @Override
    public void displayCurrentState() throws InterpreterException {
        this.repo.getProgramList().forEach(program ->
                System.out.println(program.toString() + "\n"));
    }

    @Override
    public void setProgram(IStatement statement) throws InterpreterException {

        this.repo.clear();
        this.repo.addProgram(new ProgramState(
                new ExecutionStack(),
                new SymbolTable(),
                new Output(),
                new FileTable(),
                new ConcurentHeapTable(),
                statement));

        try {
            this.repo.logProgramStateExecution(this.repo.getProgramList().get(0));
        } catch (ExecutionException | IOException | AdtException e) {
            throw new InterpreterException(e.getMessage());
        }

        if(this.displayFlag){
            this.displayCurrentState();
        }
    }

    @Override
    public void setProgramList(List<ProgramState> programList) {
        this.repo.setProgramList(programList);
    }

    @Override
    public List<ProgramState> getProgramList() {
        return this.repo.getProgramList();
    }

    @Override
    public void setDisplayFlag(boolean displayFlag) {
        this.displayFlag = displayFlag;
    }

    public IRepo getRepo() {
        return repo;
    }

    public void setRepo(IRepo repo) {
        this.repo = repo;
    }
}
