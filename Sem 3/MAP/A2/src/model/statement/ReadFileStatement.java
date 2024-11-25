package model.statement;

import model.ProgramState;
import model.exception.*;
import model.expresion.IExpression;
import model.expresion.VariableExpression;
import model.type.StringType;
import model.values.IValue;
import model.values.IntValue;
import model.values.StringValue;

import java.io.BufferedReader;

public class ReadFileStatement implements IStatement{
    IExpression expression;
    String varName;

    public ReadFileStatement(VariableExpression exp, String var) {
        this.expression = exp;
        this.varName = var;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        if(!state.getSymbolTable().isDefined(varName))
            throw new VariableNotDefinedException("Variable \""+ varName+"\" not defined");

        IValue value = expression.evaluate(state);
        if(!value.getType().equals(new StringType()))
            throw new VariableNotDefinedException("Expression evaluation must be a string");
        StringValue stringValue = (StringValue) value;
        if(!state.getFileTable().isDefined(stringValue))
            throw new FileException("File not opened");

        BufferedReader bufferedReader = state.getFileTable().lookup(stringValue);
        String line;
        try {
            line = bufferedReader.readLine();
        }catch (Exception e){
            throw new FileException("Error reading from file: " + e.getMessage());
        }
        if(line == null)
            state.getSymbolTable().give(varName, new IntValue(0));
        else{
            try{
                Integer number = Integer.parseInt(line);
                state.getSymbolTable().give(varName, new IntValue(number));
            }
            catch (NumberFormatException e){
                state.getSymbolTable().give(varName, new IntValue(0));
            }
        }
        return state;
    }

    @Override
    public String toString() {
        return "RF[" + expression.toString() + ','+ varName + ']';
    }
}
