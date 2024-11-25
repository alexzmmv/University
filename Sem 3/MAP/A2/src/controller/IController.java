package controller;

import model.exception.AdtException;
import model.exception.ExecutionException;
import model.exception.ExpressionException;
import repository.IRepo;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Scanner;

public interface IController {
    void executeOneStep() throws AdtException, ExpressionException, ExecutionException;
    void executeAll(Boolean displayFlag) throws AdtException, ExpressionException, ExecutionException;
}

