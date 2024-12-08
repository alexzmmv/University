package model.statement;

import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import exception.FileException;
import model.expresion.IExpression;
import model.type.StringType;
import model.values.IValue;
import model.values.StringValue;

import java.io.BufferedReader;

public class CloseReadFileStatement implements IStatement{
    IExpression expression;

    public CloseReadFileStatement(IExpression expression) {
        this.expression = expression;
    }


    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        if(!value.getType().equals(new StringType()))
            throw new ExpressionException("Expression evaluation must be a string");
        StringValue stringValue = (StringValue) value;
        if(!state.getFileTable().isDefined(stringValue))
            throw new FileException("File not opened");
        BufferedReader bufferedReader = state.getFileTable().lookup(stringValue);
        try {
            bufferedReader.close();
        }catch (Exception e){
            throw new FileException("Error closing file: " + e.getMessage());
        }
        state.getFileTable().remove(stringValue);
        return null;
    }

    @Override
    public String toString() {
        return "CRF[" +expression +']';
    }
}
