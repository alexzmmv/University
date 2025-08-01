package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.type.IType;


public interface IStatement {
    ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException;

    MyDictionary<String, IType> typecheck(MyDictionary<String, IType> typeEnv) throws TypeNotMatchException;

    String toString();
}