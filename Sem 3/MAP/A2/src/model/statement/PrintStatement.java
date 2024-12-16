package model.statement;

import exception.TypeNotMatchException;
import model.ProgramState;
import exception.AdtException;
import exception.ExecutionException;
import exception.ExpressionException;
import model.adts.MyDictionary;
import model.expresion.IExpression;
import model.type.IType;

public class PrintStatement implements IStatement{
    IExpression expression;

    public PrintStatement(IExpression expression) {
        this.expression = expression;
    }

    @Override
    public String toString() {
        return "print["+expression.toString()+"]";
    }

    @Override
    public MyDictionary<String, IType> typecheck(MyDictionary<String, IType>  typeEnv) throws TypeNotMatchException {
        try {
            expression.typeCheck(typeEnv);
        }
        catch (AdtException e) {
            throw new TypeNotMatchException("Print statement: " + e.getMessage());
        }
        return typeEnv;
    }

    @Override
    public ProgramState execute(ProgramState state) throws AdtException, ExpressionException, ExecutionException {
        state.getOutput().add(expression.evaluate(state));
        return null;
    }
}
