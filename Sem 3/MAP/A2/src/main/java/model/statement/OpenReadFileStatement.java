package model.statement;

import exception.*;
import model.ProgramState;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.type.IType;
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
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);

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
        return null;
     }

    @Override
    public String toString() {
        return "ORF["+ expression + ']';
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType type = null;
        try {
            type = expression.typeCheck(typeEnv);

            if(!(type instanceof StringType)){
                throw new TypeNotMatchException("OpenReadFileStatement: Expression must be a string");
            }
        } catch (AdtException e) {
            throw new TypeNotMatchException("OpenReadFileStatement: " + e.getMessage());
        }
        if(!type.equals(new StringType())){
            throw new TypeNotMatchException("OpenReadFileStatement: Expression must be a string");
        }
        return typeEnv;
    }

}
