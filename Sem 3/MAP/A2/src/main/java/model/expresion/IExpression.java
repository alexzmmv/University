package model.expresion;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.type.IType;
import model.values.IValue;
import exception.TypeNotMatchException;
public interface IExpression {
    IValue evaluate(ProgramState state) throws ExpressionException, AdtException, ExecutionException;
    String toString();
    IType typeCheck(MyDictionary<String,IType> typeEnv) throws TypeNotMatchException, AdtException;
}
