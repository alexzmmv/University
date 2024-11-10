package controller;

import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;

import java.io.IOException;

public interface IController {
    void executeOneStep() throws AdtException, ExpressionException, ExecutionException;
    void executeAll() throws AdtException, ExpressionException, ExecutionException, IOException;
}
