package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.type.BoolType;
import model.type.IType;
import model.values.BoolValue;
import model.values.IValue;

public class whileStatement implements IStatement{
    IExpression expression;
    IStatement statement;

    public whileStatement(IExpression expression, IStatement statement) {
        this.expression = expression;
        this.statement = statement;
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        IType type = null;
        try {
            type = expression.typeCheck(typeEnv);
        } catch (AdtException e) {
            throw new TypeNotMatchException("While statement: " + e.getMessage());
        }
        if(!(type instanceof BoolType)){
            throw new TypeNotMatchException("The while condition should evaluate to a Boolean Type");
        }
        statement.typecheck(typeEnv);
        return typeEnv;
    }

    @Override
    public ProgramState execute(ProgramState state) throws ExpressionException, AdtException, ExecutionException {
        IValue value = expression.evaluate(state);
        if(!(value.getType() instanceof BoolType)){
            throw new ExecutionException("The while condition should evaluate to a Boolean Type");
        }
        BoolValue boolValue = (BoolValue)value;
        if(boolValue.getVal()){
            state.getExecutionStack().push(this);
            state.getExecutionStack().push(statement);
        }
        return null;
    }

    @Override
    public String toString() {
        return "while(" + expression.toString() + "){" + statement.toString() + "}";
    }
}
