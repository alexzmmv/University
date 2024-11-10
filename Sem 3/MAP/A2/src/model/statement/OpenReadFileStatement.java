package model.statement;

import model.ProgramState;
import model.exception.AdtException;
import model.exception.ExpressionException;
import model.exception.FileException;
import model.expresion.IExpression;
import model.type.StringType;
import model.values.IValue;
import model.values.StringValue;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class OpenReadFileStatement implements IStatement{
    IExpression expression;

    public OpenReadFileStatement(IExpression varName) {
        this.expression = varName;
    }
    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException {
        IValue value = expression.evaluate(state.getSymbolTable());

        if(!value.getType().equals(new StringType())){
            throw new FileException("File name must be a string");
        }
        StringValue stringValue = (StringValue) value;
        if(state.getFileTable().isDefined( stringValue)){
            throw new FileException("File with that name already opened");
        }
        BufferedReader bufferedReader;
        try {
            bufferedReader = new BufferedReader(new FileReader(stringValue.getVal()));
        }catch (IOException e) {
            throw new FileException("Error opening file: " + e.getMessage());
        }

        state.getFileTable().put(stringValue, bufferedReader);
        return state;
     }

    @Override
    public String toString() {
        return "ORF["+ expression + ']';
    }

}
